import clips

DEFTEMPLATE_STRING = """
(deftemplate user
  (slot age (type INTEGER))
  (slot preferred_genre (type STRING))
  (slot payment (type FLOAT)))
"""

DEFRULE_STRING = """
(defrule recommend-books
  "Recommend books based on age, preferred genre, and payment range."
  (user (age ?age) (preferred_genre ?genre) (payment ?price))
  =>
  (if (and (> ?age 18) (eq ?genre "Terror")) then
    (printout t "Recommended Terror Books for Adults:" crlf)
    (printout t "- 'O Iluminado' by Stephen King ($99,00)" crlf)
    (printout t "- 'O Exorcista' by William Peter Blatty ($55,00)" crlf)
    (printout t "- 'A Assombração da Casa da Colina' by Shirley Jackson ($38,00)" crlf)
  else
    (if (and (<= ?age 18) (eq ?genre "Terror")) then
      (printout t "Recommended Terror Books for Teens:" crlf)
      (printout t "- 'Drácula' by Bram Stoker ($45,00)" crlf)
      (printout t "- 'A Casa de Adela' by Mariana Enriquez ($25,00)" crlf)
    )
  )
  (if (eq ?genre "Aventura") then
    (if (> ?price 50) then
      (printout t "Recommended Adventure Book for over $50:" crlf)
      (printout t "- 'Jurassic Park' by Michael Crichton ($40,00)" crlf)
    else
      (printout t "Recommended Adventure Books under $50:" crlf)
      (printout t "- 'As Aventuras de Huckleberry Finn' by Mark Twain ($28,00)" crlf)
      (printout t "- 'O Hobbit' by J.R.R. Tolkien ($35,00)" crlf)
    )
  )
  (if (eq ?genre "Romance") then
    (if (> ?price 50) then
      (printout t "Recommended Romance Books for over $50:" crlf)
      (printout t "- 'Orgulho e Preconceito' by Jane Austen ($30,00)" crlf)
    else
      (printout t "Recommended Romance Books under $50:" crlf)
      (printout t "- 'A Culpa é das Estrelas' by John Green ($18,00)" crlf)
      (printout t "- 'Como Eu Era Antes de Você' by Jojo Moyes ($25,00)" crlf)
    )
  )
)
"""

def get_input(prompt, type_func=str):
    """Helper function to get and convert user input."""
    while True:
        try:
            return type_func(input(prompt))
        except ValueError:
            print(f"Invalid input. Please enter a valid {type_func.__name__}.")

def main():
    environment = clips.Environment()

    environment.build(DEFTEMPLATE_STRING)
    environment.build(DEFRULE_STRING)

    age = get_input("Enter your age: ", int)
    preferred_genre = get_input("Enter your preferred genre (Romance, Terror, Aventura): ")
    payment = get_input("Price range you are willing to pay: [Choose between $1 to 100] ", float)

    template = environment.find_template('user')
    if template is None:
        raise RuntimeError("Template 'user' not found.")

    fact = template.assert_fact(age=age,
                                preferred_genre=preferred_genre,
                                payment=payment)

    assert fact['age'] == age, "Age slot mismatch."
    assert fact['preferred_genre'] == preferred_genre, "Preferred genre slot mismatch."
    assert fact['payment'] == payment, "Payment slot mismatch."

    try:
        environment.run()
    except Exception as e:
        print(f"An error occurred during execution: {e}")

if __name__ == "__main__":
    main()
