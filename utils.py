def is_safe_sql(query):
    """
    PM Requirement: Prevent destructive SQL commands.
    """
    forbidden_words = ["DROP", "DELETE", "TRUNCATE", "UPDATE", "INSERT", "ALTER"]
    for word in forbidden_words:
        if word in query.upper():
            return False
    return True