(define (my-filter pred s)
  (cond
      ((null? s) s)
      (else 
          (if (pred (car s)) 
              (append (list (car s)) (my-filter pred (cdr s))) 
              (my-filter pred (cdr s))))
  )
)


(define (interleave lst1 lst2) 
  (cond
   ((null? lst1) lst2)
   ((null? lst2) lst1)
   (else (append (list (car lst1) (car lst2)) (interleave (cdr lst1) (cdr lst2))))
  )
)

(define (accumulate joiner start n term)
  (cond
    ((= n 0) start)
    (else (joiner (term n) (accumulate joiner start (- n 1) term)))  
  )
)

(define (no-repeats lst) 
  (cond
    ((<= (length lst) 1) lst)
    (else (append (list (car lst)) (my-filter (lambda (x) (not (= x (car lst)))) (no-repeats (cdr lst)))))
  )
)
