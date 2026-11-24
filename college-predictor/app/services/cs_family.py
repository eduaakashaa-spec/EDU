"""Classification of a programme name into a computer-stream family, shared by tools/cs_stream/build_colleges.py and the page service (app/services/cs_stream.py)."""
import re


def clean_program(p):
    return re.sub(r'\s*\(\d+ Years.*$', '', p).strip()


def duration(p):
    m = re.search(r'\((\d) Years,\s*([^)]*)\)', p)
    return (int(m.group(1)), m.group(2).strip()) if m else (None, '')


def family(prog):
    """The computer-stream family of a programme name, or None when it is not a computer-stream programme."""
    p = clean_program(prog)
    low = re.sub(r'\s+', ' ', p.lower().replace('&', ' and ')).strip()          # "Electronics & Computer" reads as "electronics and computer"
    if re.search(r'architect|planning|biotech|bioinformatic|biochem|chemical|civil|mining|agricultur|metallurg|textile|mechanical engineering and', low) and not re.search(r'\bcomputer|artificial|data science', low):
        return None
    if re.search(r'\bcyber\b', low):
        return 'cyber'
    if re.search(r'business', low) and re.search(r'computer|information technology', low):
        return 'biz'
    if re.search(r'mathematics\b.*\bcomput|math.*&.*comput|computational mathematics|mathematics and scientific computing|mathematics and data|statistics and data|quantitative economics', low):
        return 'mnc'
    if re.search(r'artificial|machine learning|intelligent systems|\bai\b|data science|data engineering|data analytics|data and|computational and data|data & ', low):
        # engineering branches that only add a data-analytics label (for example Chemical Engineering with Data Analytics) are not computer-stream degrees
        if re.search(r'^(chemical|agricultural|biomedical|mechanical|civil|electrical|mining|metallurg)', low) and not re.search(r'computer', low):
            return None
        return 'aids'
    if re.search(r'electronics and computer|electrical and computer|computer and communication|computer science and design|information and communication', low):
        return 'hybrid'                                    # computing joined to electronics, communication or design
    if re.search(r'\binformation technology\b|\binformation science\b', low):
        return 'it'                                        # Information Science and Engineering (ISE) is the Karnataka name for the IT-type branch
    if re.search(r'\become\b', low):
        return 'hybrid'                                    # EComE: Electronics and Computer Engineering
    if re.search(r'^cse\b|\bcse\b', low):
        return 'core'                                      # abbreviations such as CSE and CSE - Gaming, AR and VR (the AI, cyber and business variants were caught above)
    if re.search(r'\bcomputer science|\bcomputer engineering|\bcomputing and|^computer\b', low) and not re.search(r'human computer|physics and computational', low):
        return 'core'
    if re.search(r'human computer|internet of things|\biot\b|robotics|computational (?:engineering|mechanics)|engineering and computational|mechanics and computing|electronics communication and artificial', low):
        return 'hybrid'
    return None
