
try:
    import streamlit
    import ui.dashboard
    import ui.goals
    import ui.journal
    import ui.settings
    print("IMPORTS_OK")
except Exception as e:
    print(f"IMPORT_ERROR: {e}")
