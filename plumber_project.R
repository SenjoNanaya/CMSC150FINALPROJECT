library(plumber)
library(jsonlite)

Simplex <- function(tableau, isMax = TRUE) {
    stopifnot(is.matrix(tableau))

    nrows <- nrow(tableau)
    ncols <- ncol(tableau)
    rhs_col <- ncols

    iterations <- list()
    iter <- 0

    cat("Initial Tableau:\n")
    print(round(tableau, 6))
    cat("\n-------------------------------------\n")

    # finding z column
    zcol_index <- NA
    for (j in 1:(rhs_col-1)) {
        if (tableau[nrows, j] == 1 && all(tableau[-nrows, j] == 0)) {
            zcol_index <- j
            break
        }
    }
    hasZcol <- !is.na(zcol_index)

    # var cols
    varcols <- setdiff(1:(rhs_col-1), if (hasZcol) zcol_index else integer(0))

    # a hold over from the exer (you never really should use since this solver only ever minimizes !isMax but it's still here)
    if (!isMax) {
        tableau[nrows, varcols] <- -tableau[nrows, varcols]
    }

    # storing initial tableau
    iterations[[1]] <- list(
        iteration = 0,
        tableau = round(tableau, 6),
        pivotRow = NA,
        pivotCol = NA,
        pivotElement = NA
    )

    # simplex iterations
    repeat {
        # objective row excluding RHS
        lastRow <- tableau[nrows, -rhs_col]  

        # check if all coefficients are non-negative.
        if (all(lastRow >= -1e-10)) {
          cat("Optimal solution found (all objective coefficients non-negative)\n")
          break
        }

        # pick pivot col
        pivotCol <- which.min(lastRow)

        # ratio test
        numer <- tableau[-nrows, rhs_col]
        denom <- tableau[-nrows, pivotCol]
        ratios <- numer / denom
        ratios[denom <= 1e-10] <- Inf  # CANT BE ZERO

        # check if infinite
        if (all(is.infinite(ratios))) {
            return(list(
                error = "Linear program is unbounded",
                infeasible = TRUE
            ))
        }

        # check for infeasibility (negative RHS with no valid pivots)
        if (any(numer < -1e-10) && all(ratios[numer < -1e-10] == Inf)) {
            return(list(
                error = "Linear program is infeasible",
                infeasible = TRUE
            ))
        }

        pivotRow <- which.min(ratios)
        pivotElement <- tableau[pivotRow, pivotCol]

        tableau[pivotRow, ] <- tableau[pivotRow, ] / pivotElement

        for (r in seq_len(nrows)) {
            if (r == pivotRow) next
            factor <- tableau[r, pivotCol]
            tableau[r, ] <- tableau[r, ] - factor * tableau[pivotRow, ]
        }

        iter <- iter + 1
        cat("Iteration", iter, "\n")
        cat("Pivot element:", round(pivotElement, 6),
            "at row", pivotRow, "col", pivotCol, "\n")
        print(round(tableau, 6))
        cat("\n-------------------------------------\n")

        # storing iterations to present later on the gui
        iterations[[iter + 1]] <- list(
            iteration = iter,
            tableau = round(tableau, 6),
            pivotRow = pivotRow,
            pivotCol = pivotCol,
            pivotElement = round(pivotElement, 6)
        )
    }

    # Z value (negate back if minimization)
    # ^ this does not matter anymore considering that the extra logic for minimization that used to be here has been moved to the tableau construction
    # in project_gui.py
    Z <- tableau[nrows, rhs_col]
    
    # NO NEED ANYMORE BECAUSE IT'S ALWAYS MINIMIZATION (I had so many issues realizing that I was double negating)
    #if (!isMax) {
    #    Z <- -Z  # Convert back to original minimization objective
    #}

    # number of constraints and decision variables
    n_constraints <- nrows - 1
    n_varcols <- length(varcols)
    n_decision <- n_varcols - n_constraints
    if (n_decision < 0) n_decision <- 0

    # basic solution thru finding identity columns
    var_solution <- rep(0, n_varcols)
    
    for (j in seq_along(varcols)) {
        col_x <- varcols[j]
        col <- tableau[1:n_constraints, col_x]
        
        # need to check if identity
        if (sum(abs(col - 1) < 1e-10) == 1 && sum(abs(col) < 1e-10) == (n_constraints - 1)) {
            # find which row has the 1 just like in the handout
            basic_row <- which(abs(col - 1) < 1e-10)
            if (length(basic_row) == 1) {
                var_solution[j] <- tableau[basic_row, rhs_col]
            }
        }
    }

    # split into decision variables and slack variables
    x_vals <- if (n_decision > 0) var_solution[1:n_decision] else numeric(0)
    s_vals <- if (n_constraints > 0) var_solution[(n_decision+1):n_varcols] else numeric(0)

    # NO NEED ANYMORE SINCE I DECIDED TO NOT INCLUDE THIS ANYMORE SINCE IT WAS A HASSLE TO LABEL AND EXPLAIN THIS PORTION WHEN IT'S NOT NEEDED TO PROJECT SPECS
    #finalSolution <- c(x_vals, s_vals, Z)
    #names(finalSolution) <- c(
    #    if (n_decision > 0) paste0("x", 1:n_decision) else character(0),
    #    if (n_constraints > 0) paste0("s", 1:n_constraints) else character(0),
    #    "Z"
    #)

    return(list(
        finalTableau = round(tableau, 6),
        #finalSolution = round(finalSolution, 6),
        Z = round(Z, 6),
        iterations = iterations,
        infeasible = FALSE
    ))
}


# helper function! convert incoming JSON "tableau" (list of rows) into numeric matrix
make_tableau_from_list <- function(tbl_list) {
  # issues awhile ago where tableau was sometimes not a list of rows (holdover from debugging)
  if (!is.list(tbl_list)) stop("tableau must be a list of rows")
  rows <- lapply(tbl_list, function(r) as.numeric(unlist(r)))
  nr <- length(rows)
  if (nr == 0) stop("empty tableau")
  nc <- length(rows[[1]])
  mat <- matrix(0, nrow = nr, ncol = nc)
  for (i in seq_len(nr)) {
    if (length(rows[[i]]) != nc) stop("all rows must have equal length")
    mat[i, ] <- rows[[i]]
  }
  return(mat)
}

# PLUMBER FUNCTIONS
#* @post /simplex
#* @json
function(req, res){
  body <- jsonlite::fromJSON(req$postBody, simplifyVector = FALSE)
  # expected keys: tableau (list of rows) , isMax (bool)
  if (is.null(body$tableau)) {
    res$status <- 400
    return(list(error="missing 'tableau' in body"))
  }
  isMax <- ifelse(is.null(body$isMax), TRUE, as.logical(body$isMax))
  # convert to numeric matrix
  mat <- tryCatch(make_tableau_from_list(body$tableau), error = function(e) e)
  if (inherits(mat, "error")) {
    res$status <- 400
    return(list(error=mat$message))
  }

  # call Simplex safely
  out <- tryCatch({
    Simplex(mat, isMax = isMax)
  }, error = function(e) {
    list(error = paste0("Simplex error: ", e$message))
  })

  # if out is an error-like list, return 500
  if (!is.null(out$error)) {
    res$status <- 400
    return(out)
  }

  # ensure output is JSON-serializable (CMSC 22 moment)
  out$finalTableau <- as.data.frame(out$finalTableau)
  return(out)
}