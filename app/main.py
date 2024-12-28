from fasthtml.common import * # type: ignore
from fasthtml.common import (
    Form, Label, Input, Button, Html, Head, Body, Div, P, Title, Titled, A, Link, Meta, H1
)
import re

# for docker
app, rt = fast_app(static_path="static") # type: ignore

# for local
# app, rt = fast_app(static_path="app/static") # type: ignore

temperature_form = Form(
    method="post",
    action="/convert"
    )(
        Label("Temperature", cls="select", style="padding-bottom: 0.35rem; font-variant-caps: petite-caps;"),
        Input(
            name="temperature",
            type="text",
            pattern="^-?\d+(\.\d+)?$",
            title="\nEnter a valid floating-point number",
            required=True,
            cls="select",
            style="margin-bottom: 1.5rem; width: clamp(225px, 20vw, 400px);"
        ),
        Button("Fahrenheit → Celsius",
            name="conversion",
            value="fc",
            type="submit",
            style="margin: 1rem; width: clamp(225px, 20vw, 400px);"
        ),
        Button("Fahrenheit → Kelvin",
            name="conversion",
            value="fk",
            type="submit",
            style="margin: 1rem; width: clamp(225px, 20vw, 400px);"
        ),
        Button("Celsius → Fahrenheit",
            name="conversion",
            value="cf",
            type="submit",
            style="margin: 1rem; width: clamp(225px, 20vw, 400px);"
        ),
        Button("Celsius → Kelvin",
            name="conversion",
            value="ck",
            type="submit",
            style="margin: 1rem; width: clamp(225px, 20vw, 400px);"
        ),
        Button("Kelvin → Celsius",
            name="conversion",
            value="kc",
            type="submit",
            style="margin: 1rem; width: clamp(225px, 20vw, 400px);"
        ),
        Button("Kelvin → Fahrenheit",
            name="conversion",
            value="kf",
            type="submit",
            style="margin: 1rem; width: clamp(225px, 20vw, 400px);"
        ),
        cls="container",
    )

@rt("/")
def homepage():
    return Html(
        Head(
            Title("Temperature Converter"),
            Meta(name="viewport", content="width=device-width, initial-scale=1"),
            Link(rel="stylesheet", href="styles.css"),
            Link(rel="icon", href="images/favicon.ico", type="image/x-icon"),
            Link(rel="icon", href="images/favicon.png", type="image/png"),
        ),
        Body(temperature_form)
    )

@rt("/convert", methods=["POST"])
def convert_temperature(temperature:str, conversion:str):
    # validation:
    if not re.match(r"^-?\d+(\.\d+)?$", temperature):
        return Html(
            Head(
                Title("Error"),
                Meta(name="viewport", content="width=device-width, initial-scale=1"),
                Link(rel="stylesheet", href="styles.css"),
                Link(rel="icon", href="images/favicon.ico", type="image/x-icon"),
                Link(rel="icon", href="images/favicon.png", type="image/png"),
            ),
            Body(
                Titled("Invalid Input"),
                P("Please enter a valid floating-point number for the temperature."),
                Button(
                    A("Return to Form", href="/"),
                ),
            )
        )

    # temperature conversion to float:
    temperature_float = float(temperature)

    # conversion(calculation) logic
    if conversion == "kc":
        kc = temperature_float + 273.15
        result = f"{temperature_float}° Kelvin equals to {kc:.2f}°C"
    elif conversion == "kf":
        kf = ((temperature_float - 273.15) * (9/5)) + 32
        result = f"{temperature_float}° Kelvin equals to {kf:.2f}°F"
    elif conversion == "fc":
        fc = (temperature_float - 32) * (5/9)
        result = f"{temperature_float}° Fahrenheit equals to {fc:.2f}°C"
    elif conversion == "fk":
        fk = ((temperature_float - 32) * (5/9)) + 273.15
        result = f"{temperature_float}° Fahrenheit equals to {fk:.2f}°K"
    elif conversion == "cf":
        cf = (temperature_float * (9/5)) + 32
        result = f"{temperature_float}° Celsius equals to {cf:.2f}°F"
    elif conversion == "ck":
        ck = temperature_float - 273.15
        result = f"{temperature_float}° Celsius equals to {ck:.2f}°K"


    return Html(
        Head(
            Title("Conversion Results"),
            Meta(name="viewport", content="width=device-width, initial-scale=1"),
            Link(rel="stylesheet", href="styles.css"),
            Link(rel="icon", href="images/favicon.ico", type="image/x-icon"),
            Link(rel="icon", href="images/favicon.png", type="image/png"),
        ),
        Body(
            H1("Conversion Results"),
            P(result),
            Button(
                A("Return to Form", href="/"),
                style="margin-top: 1.25rem;",
            )
        )
    )

if __name__ == '__main__':
    # Important: Use host='0.0.0.0' to make the server accessible outside the container
    serve(host='0.0.0.0', port=5002) # type: ignore