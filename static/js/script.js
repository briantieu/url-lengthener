const button_click = () => {
    const txt_data = document.getElementById('url-output')
    const value = txt_data.value
    navigator.clipboard.writeText(value)
}