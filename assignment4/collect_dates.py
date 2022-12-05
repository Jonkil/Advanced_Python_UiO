import re
from typing import Tuple

## -- Task 3 (IN3110 optional, IN4110 required) -- ##

# create array with all names of months
month_names = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

# create array with all numbers of months as strings
month_numbers = [
    "01", "1",
    "02", "2",
    "03", "3",
    "04", "4",
    "05", "5",
    "06", "6",
    "07", "7",
    "08", "8",
    "09", "9",
    "10",
    "11",
    "12",
]

# create array with all numbers of days as strings
day_numbers = [str(i) for i in range(1,32)]+['0'+str(i) for i in range(1,10)]

# create non-capturing group substrings for regexp patterns
choose_month_str = '(?:'+'|'.join(month_names)+')'
choose_month_num_str = '(?:'+'|'.join(month_numbers)+')'
choose_day_str = '(?:'+'|'.join(day_numbers)+')'

def get_date_patterns() -> Tuple[str, str, str]:
    """Return strings containing regex pattern for year, month, day
    arguments:
        None
    return:
        year, month, day (tuple): Containing regular expression patterns for each field
    """

    # Regex to capture days, months and years with numbers
    # year should accept a 4-digit number between at least 1000-2029
    year = r"(?P<year>[1-2]\d{3})"
    
    # month should accept month names or month numbers
    month = rf"(?P<month>{choose_month_str}|{choose_month_num_str})"
    
    # day should be a number, which may or may not be zero-padded
    day = rf"(?P<day>{choose_day_str})"

    return year, month, day


def convert_month(s: str) -> str:
    """Converts a string month to number (e.g. 'September' -> '09'.

    You don't need to use this function,
    but you may find it useful.

    arguments:
        month_name (str) : month name
    returns:
        month_number (str) : month number as zero-padded string
    """
    # If already digit do nothing
    if s.isdigit():
        month_number = str(s).zfill(2)
    else:
        # Convert to number as string
        month_number = str(month_names.index(s)+1).zfill(2)
    
    return month_number


def zero_pad(n: str):
    """zero-pad a number string

    turns '2' into '02'

    You don't need to use this function,
    but you may find it useful.
    """
    return n.zfill(2)


def convert_date(d: str) -> str:
    """Accepts date as '2022/November/7' and
        - converts month name to month number
        - zero-pads the day number

    Args:
        d (str): date in the described format 

    Returns:
        str: date in the required format, ex. 2022/11/07.
    """
    d_ = d.split('/')
    d_[1] = convert_month(d_[1])
    d_[2] = zero_pad(d_[2])
    return '/'.join(d_)


def find_dates(text: str, output: str = None) -> list:
    """Finds all dates in a text using reg ex

    arguments:
        text (string): A string containing html text from a website
    return:
        dates (list): A list with all the dates found
    """
    year, month, day = get_date_patterns()

    # Date on format YYYY/MM/DD - ISO
    ISO = r"[1-2]\d{3}-"+choose_month_num_str+r"-\d{2}"

    # Date on format DD/MM/YYYY
    DMY = r"\d{1,2}\s"+choose_month_str+r"\s[1-2]\d{3}"

    # Date on format MM/DD/YYYY
    MDY = choose_month_str+r"\s\d{1,2},\s[1-2]\d{3}"

    # Date on format YYYY/MM/DD
    YMD = r"[1-2]\d{3}\s"+choose_month_str+r"\s\d{1,2}"

    # make a dictionary to keep consistency between 
    # formats and their names
    formats_dict = {"ISO":ISO, "DMY":DMY, "MDY":MDY, "YMD":YMD}   
    # list with all supported formats
    formats = list(formats_dict.values())
    format_names = list(formats_dict.keys())
    
    # we need to find all dates in order of occurrence
    wiki_date_pat = re.compile('('+')|('.join(list(formats))+')')
    
    dates = []

    # find all dates in any format in text
    dates__ = re.findall(wiki_date_pat,text)
    # dates__ is a list of tuples of length 4
    # one element in a tuple is a date captured 
    # by one of the formats (ISO, DMY, MDY, YMD), 
    # other three elements are ''
    
    for tuple_ in dates__:
        for i, date in enumerate(tuple_):
            if date:
                if format_names[i]=='ISO':
                    d = re.sub(rf"{year}-{month}-{day}", r"\1/\2/\3",date)
                elif format_names[i]=='DMY':
                    d = re.sub(rf"{day}\s{month}\s{year}", r"\3/\2/\1",date)
                elif format_names[i]=='MDY':
                    d = re.sub(rf"{month}\s{day},\s{year}", r"\3/\1/\2",date)
                elif format_names[i]=='YMD':
                    d = re.sub(rf"{year}\s{month}\s{day}", r"\1/\2/\3",date)
                d = convert_date(d)
                # if the date is already added, ignore
                # keep unique dates
                if not d in dates:
                    dates.append(d)
        
    # Write to file if wanted
    if output:
        print(f"Writing to: {output}")
        # if output is specified, dates are printed to a
        # txt file with the name in `output`
        with open(output,'w',encoding = 'utf-8') as f:
            for d in dates:
                f.write(d + "\n")
        return None

    return dates
