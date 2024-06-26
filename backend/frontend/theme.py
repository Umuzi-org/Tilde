PRIMARY_COLOUR = "indigo"
TEXT_COLOUR = "gray"

styles = {
    # buttons
    "button_primary_small": f"rounded bg-{PRIMARY_COLOUR}-600 px-2 py-1 text-xs font-semibold text-white shadow-sm hover:bg-{PRIMARY_COLOUR}-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-{PRIMARY_COLOUR}-600 disabled:text-opacity-70 disabled:bg-opacity-50",
    #
    "button_secondary_small": f"rounded bg-white px-2 py-1 text-xs font-semibold text-gray-900 shadow-sm hover:bg-gray-100 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600 ring-1 ring-inset ring-gray-300",
    # headings
    "heading1": f"text-2xl font-bold text-{TEXT_COLOUR}-600",
    "heading2": f"text-xl font-bold text-{TEXT_COLOUR}-600",
    "heading3": f"text-l font-bold text-{TEXT_COLOUR}-600",
    # link
    "link": f"text-{PRIMARY_COLOUR}-600 hover:text-{PRIMARY_COLOUR}-500 focus:text-{PRIMARY_COLOUR}-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-{PRIMARY_COLOUR}-500 underline underline-offset-2",
    # input
    "input_small": f"border border-gray-300 rounded-md shadow-sm text-sm focus:ring-{PRIMARY_COLOUR}-500 focus:border-{PRIMARY_COLOUR}-500 px-2 py-1 my-2 w-full",
    "label_small": f"text-sm font-medium text-gray-700",
    # alerts
    "alert_debug": f"bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative",
    "alert_info": f"bg-{PRIMARY_COLOUR}-100 border border-{PRIMARY_COLOUR}-400 text-{PRIMARY_COLOUR}-700 px-4 py-3 rounded relative",
    "alert_warning": f"bg-gray-100 border border-gray-400 text-gray-700 px-4 py-3 rounded relative",
    "alert_success": f"bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative",
    "alert_error": f"bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative",
    "field_error": f"text-red-700",
    "secondary_header_container": "bg-white shadow py-5 flex items-center sticky top-[65px] w-full z-40 flex-wrap",
    "badge_secondary": "text-black text-opacity-90 text-xs font-light font-['Poppins'] leading-relaxed tracking-tight bg-[gray] bg-neutral-800 bg-opacity-10 rounded-md p-0.5 px-2"
}
