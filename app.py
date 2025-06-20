from shiny import App, ui, render, reactive
import math

def rankine_earth_pressures(phi_deg):
    """
    Calculates Rankine's earth pressure coefficients for a vertical wall and horizontal backfill.
    
    Parameters:
    - phi_deg: Internal angle of friction of the soil in degrees.

    Returns:
    - A dictionary with at-rest (Ko), active (Ka), and passive (Kp) earth pressure coefficients.
    """
    phi_rad = math.radians(phi_deg)
    
    # Active earth pressure coefficient
    Ka = (1 - math.sin(phi_rad)) / (1 + math.sin(phi_rad))
    
    # Passive earth pressure coefficient
    Kp = (1 + math.sin(phi_rad)) / (1 - math.sin(phi_rad))
    
    # At-rest earth pressure coefficient (using Jaky's empirical formula)
    Ko = 1 - math.sin(phi_rad)
    
    return {"Ka": Ka, "Kp": Kp, "Ko": Ko}

app_ui = ui.page_sidebar(
    #ui.panel_title("Rankine Earth Pressure Calculator"),
    ui.sidebar(
        ui.h3("Input Parameters"),
        ui.input_slider(
            "phi",
            "Internal Angle of Friction (φ°)",
            min=0,
            max=45,
            value=30,
            step=1
        ),
        ui.tags.hr(),
        ui.p("Enter the soil's internal angle of friction (φ) to calculate Rankine's earth pressure coefficients.")
    ),
    ui.card(
        ui.card_header("Earth Pressure Coefficients"),
        ui.output_text_verbatim("explanation"),
        ui.layout_columns(
            ui.value_box(
                "Active Pressure Coefficient (Ka)",
                ui.output_text("ka_value"),
                showcase=ui.tags.i(class_="fa-solid fa-arrow-right", style="font-size: 2rem;"),
                theme="primary"
            ),
            ui.value_box(
                "At-Rest Pressure Coefficient (Ko)",
                ui.output_text("ko_value"),
                showcase=ui.tags.i(class_="fa-solid fa-equals", style="font-size: 2rem;"),
                theme="secondary"
            ),
            ui.value_box(
                "Passive Pressure Coefficient (Kp)",
                ui.output_text("kp_value"),
                showcase=ui.tags.i(class_="fa-solid fa-arrow-left", style="font-size: 2rem;"),
                theme="success"
            ),
        ),
        ui.card_footer("Based on Rankine's earth pressure theory for a vertical wall and horizontal backfill")
    )
)

def server(input, output, session):
    @reactive.calc
    def get_coefficients():
        return rankine_earth_pressures(input.phi())
    
    @render.text
    def ka_value():
        return f"{get_coefficients()['Ka']:.4f}"
    
    @render.text
    def ko_value():
        return f"{get_coefficients()['Ko']:.4f}"
    
    @render.text
    def kp_value():
        return f"{get_coefficients()['Kp']:.4f}"
        
    @render.text
    def explanation():
        phi = input.phi()
        return f"Results for soil with φ = {phi}°:"

app = App(app_ui, server)
