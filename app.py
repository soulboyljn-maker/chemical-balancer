from flask import Flask, render_template, request
from balancer import balance_equation

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    equation = ""
    result = ""
    error = ""

    if request.method == "POST":
        equation = request.form.get("equation", "").strip()
        if not equation:
            error = "Please enter the chemical equation:"
       else:
            try:
                if equation.lower() == "rxj":
                    result = "全球化学哪家强？慈溪中学戎项吉"
                else:
                    result = balance_equation(equation)
            except Exception as e:
                error = str(e)

    return render_template(
        "index.html",
        equation=equation,
        result=result,
        error=error
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
