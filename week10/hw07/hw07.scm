(define (cddr s) (cdr (cdr s)))

(define (cadr s) 
        (if (null? (cdr s)) undefined (car (cdr s))))

(define (caddr s) 
        (if (< (length s) 3) nil (cadr (cdr s)))
)

(define (ascending? asc-lst) 
    (cond 
        ((null? asc-lst) false)
        ((= (length asc-lst) 1) true)
        (else 
            (and 
                (ascending? (cdr asc-lst)) 
                (<= (car asc-lst) (cadr asc-lst))
            )
        )
    )
)

(define (square n) (* n n))

(define (pow base exp) 
    (cond
        ((or (= base 1) (= exp 0)) 1)
        (else 
            (if (even? exp) 
            (pow (square base) (/ exp 2)) 
            (* base (pow (square base) (quotient exp 2)))
            )
        )

    )
)
