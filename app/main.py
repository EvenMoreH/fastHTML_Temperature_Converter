from fasthtml.common import * # type: ignore
from fasthtml.common import (Form, Fieldset, Label, Input, Button, Html, Head, Body, Div, P, Title, Titled, A)
import re

app, rt = fast_app() # type: ignore

temperature_form = Form(
    method = "post",
    action = "/convert"
    )(
    Fieldset(
        Label("Temperature", Input(
            name="temperature",
            type="text",
            pattern="^-?\d+(\.\d+)?$",  # Used as Regex for a float with optional negative sign
            title="\nEnter a valid floating-point number",
            required=True
            )
        ),
        style="padding: 10px; font-variant-caps: all-petite-caps; font-size: 24"
    ),
    Div(
        Button("Kelvin -> Celsius", name="conversion", value="kc", type="submit"),
        style="padding: 10px"
    ),
    Div(
        Button("Kelvin -> Fahrenheit", name="conversion", value="kf", type="submit"),
        style="padding: 10px"
    ),
    Div(
        Button("Fahrenheit -> Celsius", name="conversion", value="fc", type="submit"),
        style="padding: 10px"
    ),
    Div(
        Button("Fahrenheit -> Kelvin", name="conversion", value="fk", type="submit"),
        style="padding: 10px"
    ),
    Div(
        Button("Celsius -> Fahrenheit", name="conversion", value="cf", type="submit"),
        style="padding: 10px"
    ),
    Div(
        Button("Celsius -> Kelvin", name="conversion", value="ck", type="submit"),
        style="padding: 10px"
    ),
)

@rt("/")
def homepage():
    return Html(
        Head(
            Title("Temperature Converter")
        ),
        Body(
            Div(
                temperature_form,
            )
        )
    )

@rt("/convert", methods=["POST"])
def convert_temperature(temperature:str, conversion:str):
    # validation:
    if not re.match(r"^-?\d+(\.\d+)?$", temperature):
        return Html(
            Head(
                Title("Error")
            ),
            Body(
                Titled("Invalid Input"),
                P("Please enter a valid floating-point number for the temperature."),
                Button(
                    A("Return to Form", href="/"),
                    style="padding: 10px"
                )
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
            Title("Conversion Results")
        ),
        Body(
            Titled("Conversion Results"),
            P(result),
            Button(
                A("Return to Form", href="/"),
                style="padding: 10px"
            )
        )
    )

if __name__ == '__main__':
    # Important: Use host='0.0.0.0' to make the server accessible outside the container
    serve(host='0.0.0.0', port=5001) # type: ignore