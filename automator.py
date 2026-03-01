from automation_core import (
	get_message, get_numbers, get_driver,
	login_whatsapp, send_messages, print_intro
)

def main():
	print_intro()
	message = get_message()
	numbers = get_numbers()
	print(f"\nFound {len(numbers)} numbers in the file.")
	driver = get_driver()
	login_whatsapp(driver)
	send_messages(driver, numbers, message)
	driver.close()
	print("\nAll done! Thanks for using WhatsApp Bulk Messenger.")

if __name__ == "__main__":
	main()