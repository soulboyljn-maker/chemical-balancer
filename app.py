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
                result = balance_equation(equation)
            except Exception as e:
                import traceback
                traceback.print_exc()
                error = str(e)

    return render_template(
        "index.html",
        equation=equation,
        result=result,
        error=error
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
