from aiogram.utils.formatting import Bold, as_list, as_marked_section


categories = ['Еда', 'Напитки']

description_for_info_pages = {
    "main": "Welcome to our shop!",
    "about": "Vogue Vista.\nOperating hours: 24 hours a day.",
    "payment": as_marked_section(
        Bold("Payment options:"),
        "With a card in the bot",
        "Upon receipt of the card/cash",
        "In the establishment",
        marker="✅ ",
    ).as_html(),
    "shipping": as_list(
        as_marked_section(
            Bold("Delivery/Order Options:"),
            "Courier",
            "Self-pickup (I'll run and pick it up now)",
            "I’ll eat at your place (I’ll come running now)",
            marker="✅ ",
        ),
        as_marked_section(Bold("Not Allowed:"), "Mail", "Pigeons", marker="❌ "),
        sep="\n----------------------\n",
    ).as_html(),
    'catalog': 'Categories:',
    'cart': 'There is nothing in the cart!'
}