from datetime import datetime, timedelta

def get_monday(date):
    """
    Returns the date of the Monday of the week containing the given date.
    
    Args:
        date (datetime): The input date
        
    Returns:
        datetime: The date of the Monday of that week
    """
    return date - timedelta(days=date.weekday())

# Test program
def main():
    # Parse the input date string
    test_date = datetime.strptime('2025-07-03', '%Y-%m-%d')
    
    # Get the Monday of that week
    monday = get_monday(test_date)
    
    # Print the result
    print(f"Input date: {test_date.strftime('%Y-%m-%d')}")
    print(f"Monday of that week: {monday.strftime('%Y-%m-%d')}")

if __name__ == "__main__":
    main()
