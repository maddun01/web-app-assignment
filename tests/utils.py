def clear_selected_table(model):
    """Deletes all records in a given table"""
    model.query.delete()
