import streamlit as st
import pandas as pd
from collections import Counter
from contextlib import suppress
from datetime import date

from api_client import (
    check_backend, create_employee, get_all_employees, update_employee, delete_employee,
    create_asset, get_all_assets, update_asset, delete_asset, assign_asset, return_asset,
    get_all_tickets, create_ticket, assign_technician, resolve_ticket, change_ticket_status,
)

st.set_page_config(page_title="IT Asset & Service Management", page_icon="💻", layout="wide", initial_sidebar_state="expanded")
WF = "ticket_workflow_message"


def html(markup):
    st.markdown(markup, unsafe_allow_html=True)


# Theme: one rule per line, ordered layout -> text -> inputs -> buttons -> cards -> tabs (later rules win ties).
html("""<style>
[data-testid="stAppViewContainer"]{background:#f3f6fb!important}
[data-testid="stMain"]{background:#f3f6fb!important;color:#18263a}
[data-testid="stHeader"]{background:transparent!important}
[data-testid="stMainBlockContainer"]{padding-top:1.5rem;padding-bottom:3rem;max-width:1500px}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#14243a 0%,#203c59 100%)!important}
[data-testid="stSidebar"] *{color:#eef5ff}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p{color:#c7d5e5}
[data-testid="stSidebar"] [data-testid="stRadio"] label{border-radius:9px;padding:7px 9px}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover{background:rgba(255,255,255,.09)}
[data-testid="stSidebar"] hr{border-color:rgba(255,255,255,.18)}
[data-testid="stMain"] :is(h1,h2,h3,h4,h5,h6){color:#18263a}
[data-testid="stMain"] [data-testid="stMarkdownContainer"] > :is(p,ul,ol){color:#26364b}
[data-testid="stMain"] [data-testid="stWidgetLabel"],[data-testid="stMain"] [data-testid="stWidgetLabel"] *,[data-testid="stMain"] [data-testid="stCheckbox"] label,[data-testid="stMain"] [data-testid="stCheckbox"] label *,[data-testid="stMain"] [data-testid="stRadio"] label,[data-testid="stMain"] [data-testid="stRadio"] label *,[data-testid="stMain"] [data-testid="stFileUploaderDropzone"] *,[data-testid="stMain"] [data-testid="stMultiSelect"] label,[data-testid="stMain"] [data-testid="stSelectbox"] label{color:#344256!important}
[data-testid="stCaptionContainer"],[data-testid="stCaptionContainer"] p{color:#64748b!important}
[data-testid="stMain"] [data-baseweb="tab-panel"]{color:#18263a!important}
[data-testid="stMain"] [data-baseweb="base-input"]{background-color:#fff!important;border-color:#cbd5e1!important;border-radius:9px!important;box-shadow:none!important}
[data-testid="stMain"] input,[data-testid="stMain"] textarea,[data-testid="stMain"] [data-baseweb="select"] input{color:#172235!important;-webkit-text-fill-color:#172235!important;caret-color:#2f6fed!important;background-color:#fff!important;background:#fff!important;opacity:1!important}
[data-testid="stMain"] input::placeholder,[data-testid="stMain"] textarea::placeholder{color:#8391a5!important;-webkit-text-fill-color:#8391a5!important;opacity:1!important}
[data-testid="stMain"] [data-baseweb="select"] div[role="combobox"],[data-testid="stMain"] [data-baseweb="select"] span,[data-testid="stMain"] [data-baseweb="select"] svg{color:#172235!important;fill:#526176!important}
[data-baseweb="popover"] [role="listbox"],[data-baseweb="popover"] [data-baseweb="menu"]{background:#fff!important;color:#18263a!important}
[data-baseweb="popover"] [role="option"],[data-baseweb="popover"] [role="option"] *{color:#18263a!important}
[data-testid="stMain"] [data-testid="stBaseButton-primary"],[data-testid="stMain"] button[kind="primary"],[data-testid="stMain"] [data-testid="stFormSubmitButton"] button{background:#2f6fed!important;color:#fff!important;border:1px solid #2f6fed!important;border-radius:9px!important;font-weight:650!important;min-height:2.55rem;opacity:1}
[data-testid="stMain"] [data-testid="stBaseButton-primary"]:hover,[data-testid="stMain"] button[kind="primary"]:hover,[data-testid="stMain"] [data-testid="stFormSubmitButton"] button:hover{background:#245bd0!important;border-color:#245bd0!important;color:#fff!important}
[data-testid="stMain"] [data-testid="stBaseButton-secondary"],[data-testid="stMain"] button[kind="secondary"]{background:#fff!important;color:#26364b!important;border:1px solid #cbd5e1!important;border-radius:9px!important;font-weight:600!important}
[data-testid="stMain"] [data-testid="stBaseButton-secondary"] *,[data-testid="stMain"] button[kind="secondary"] *{color:#26364b!important}
[data-testid="stMain"] [data-testid="stBaseButton-secondary"]:hover,[data-testid="stMain"] button[kind="secondary"]:hover{background:#eef4ff!important;border-color:#9bbcfb!important}
[data-testid="stMain"] button:disabled{opacity:.58!important;cursor:not-allowed!important}
div[data-testid="stMetric"]{background:#fff!important;padding:17px 18px;border:1px solid #dbe4ef;border-radius:14px;box-shadow:0 4px 14px rgba(25,52,80,.04)}
div[data-testid="stMetricLabel"],div[data-testid="stMetricLabel"] *{color:#607087!important;font-weight:600}
div[data-testid="stMetricValue"],div[data-testid="stMetricValue"] *{color:#14243a!important;font-weight:780}
div[data-testid="stForm"]{background:#fff!important;color:#18263a!important;border:1px solid #dbe4ef;border-radius:13px;padding:16px}
div[data-testid="stExpander"]{border:1px solid #dbe4ef;border-radius:12px;background:#fff!important}
div[data-testid="stExpander"] summary,div[data-testid="stExpander"] summary *{color:#26364b!important}
div[data-testid="stDataFrame"]{background:#142a43!important;border:1px solid #294663!important;border-radius:12px;overflow:hidden;box-shadow:0 5px 16px rgba(19,34,56,.10)}
[data-testid="stAlert"]{border-radius:10px!important}
[data-testid="stAlert"] p,[data-testid="stAlert"] [data-testid="stMarkdownContainer"]{color:#26364b!important}
.brand-mark{font-size:2rem;line-height:1.2}
.brand-title{font-size:1.05rem;font-weight:750;color:#fff;margin:0}
.brand-subtitle{font-size:.76rem;color:#bed0e3;margin-top:3px}
.eyebrow{font-size:.72rem;font-weight:750;letter-spacing:.12em;color:#dceaff;text-transform:uppercase}
.hero{background:linear-gradient(110deg,#17324d 0%,#2e607b 68%,#2a8b9a 100%);border-radius:18px;padding:26px 30px;margin-bottom:22px;box-shadow:0 8px 25px rgba(25,52,80,.12)}
.hero h1{color:#fff!important;font-size:1.85rem;margin:7px 0 8px 0;font-weight:760}
.hero p{color:#e2edf8!important;font-size:.97rem;margin:0}
.section-title{font-size:1.2rem;font-weight:750;color:#18263a;margin:.25rem 0 .75rem}
.muted{color:#64748b;font-size:.9rem}
.status-pill{display:inline-block;padding:4px 10px;border-radius:999px;background:#e8f1ff;color:#2058a6!important;font-size:.78rem;font-weight:750}
.small-note{border-left:3px solid #39b8c8;padding:8px 12px;background:#eef9fb;border-radius:0 8px 8px 0;color:#345264!important;font-size:.9rem}
.small-note b,.small-note strong{color:#203b4a!important}
@media (max-width:768px){.hero{padding:20px}.hero h1{font-size:1.5rem}}
.stApp [data-testid="stTextInput"] input,.stApp [data-testid="stNumberInput"] input,.stApp [data-testid="stDateInput"] input,.stApp [data-testid="stTimeInput"] input,.stApp [data-testid="stTextArea"] textarea,.stApp [data-baseweb="input"] input,.stApp [data-baseweb="textarea"] textarea{background:#fff!important;background-color:#fff!important;color:#172235!important;-webkit-text-fill-color:#172235!important;caret-color:#2563eb!important;opacity:1!important;color-scheme:light!important}
.stApp [data-testid="stTextInput"] [data-baseweb="input"] > div,.stApp [data-testid="stNumberInput"] [data-baseweb="input"] > div,.stApp [data-testid="stDateInput"] [data-baseweb="input"] > div,.stApp [data-testid="stTimeInput"] [data-baseweb="input"] > div,.stApp [data-testid="stTextArea"] [data-baseweb="textarea"] > div,.stApp [data-baseweb="input"] > div,.stApp [data-baseweb="textarea"] > div{background:#fff!important;background-color:#fff!important;border:1px solid #cbd5e1!important;border-radius:9px!important;box-shadow:none!important}
.stApp [data-testid="stSelectbox"] [data-baseweb="select"] > div,.stApp [data-testid="stMultiSelect"] [data-baseweb="select"] > div,.stApp [data-baseweb="select"] > div{background:#fff!important;background-color:#fff!important;color:#172235!important;border-color:#cbd5e1!important;border-radius:9px!important;box-shadow:none!important}
.stApp [data-testid="stSelectbox"] [data-baseweb="select"] *,.stApp [data-testid="stMultiSelect"] [data-baseweb="select"] *,.stApp [data-baseweb="select"] [role="combobox"],.stApp [data-baseweb="select"] span{color:#172235!important;-webkit-text-fill-color:#172235!important}
.stApp [data-baseweb="select"] svg{fill:#526176!important;color:#526176!important}
.stApp [data-testid="stTextInput"] input::placeholder,.stApp [data-testid="stNumberInput"] input::placeholder,.stApp [data-testid="stTextArea"] textarea::placeholder,.stApp [data-baseweb="input"] input::placeholder,.stApp [data-baseweb="textarea"] textarea::placeholder{color:#7b8798!important;-webkit-text-fill-color:#7b8798!important;opacity:1!important}
.stApp [data-testid="stTextInput"]:focus-within [data-baseweb="input"] > div,.stApp [data-testid="stNumberInput"]:focus-within [data-baseweb="input"] > div,.stApp [data-testid="stDateInput"]:focus-within [data-baseweb="input"] > div,.stApp [data-testid="stTextArea"]:focus-within [data-baseweb="textarea"] > div,.stApp [data-testid="stSelectbox"]:focus-within [data-baseweb="select"] > div,.stApp [data-testid="stMultiSelect"]:focus-within [data-baseweb="select"] > div{border-color:#2f6fed!important;box-shadow:0 0 0 2px rgba(47,111,237,.16)!important}
.stApp [data-testid="stFormSubmitButton"] button *,.stApp [data-testid="stBaseButton-primary"] *,.stApp button[kind="primary"] *{color:#fff!important;-webkit-text-fill-color:#fff!important}
.stApp [data-baseweb="popover"],.stApp [data-baseweb="popover"] [role="listbox"],.stApp [data-baseweb="popover"] [data-baseweb="menu"],.stApp [data-baseweb="popover"] [role="option"]{background:#fff!important;color:#172235!important}
.stApp [data-baseweb="popover"] [role="option"] *{color:#172235!important}
.stApp div[data-testid="stTabs"] [role="tablist"]{display:flex!important;gap:8px!important;padding:7px!important;background:#e7edf5!important;border:1px solid #d3dce8!important;border-bottom:1px solid #cbd5e1!important;border-radius:12px 12px 0 0!important}
.stApp div[data-testid="stTabs"] [role="tablist"] button[role="tab"]{background:#dbe3ee!important;color:#26364b!important;-webkit-text-fill-color:#26364b!important;border:1px solid #c4d0df!important;border-bottom:3px solid transparent!important;border-radius:9px!important;padding:.65rem 1rem!important;margin:0!important;font-weight:650!important;box-shadow:none!important;opacity:1!important;outline:none!important}
.stApp div[data-testid="stTabs"] [role="tablist"] button[role="tab"] *,.stApp div[data-testid="stTabs"] [role="tablist"] button[role="tab"] p,.stApp div[data-testid="stTabs"] [role="tablist"] button[role="tab"] span{color:inherit!important;-webkit-text-fill-color:currentColor!important;opacity:1!important}
.stApp div[data-testid="stTabs"] [role="tablist"] button[role="tab"]:hover{background:#cbdcf5!important;color:#17324d!important;-webkit-text-fill-color:#17324d!important;border-color:#9db8dd!important}
.stApp div[data-testid="stTabs"] [role="tablist"] button[role="tab"][aria-selected="true"]{background:#17324d!important;color:#fff!important;-webkit-text-fill-color:#fff!important;border:1px solid #17324d!important;border-bottom:3px solid #39b8c8!important;border-radius:9px!important;box-shadow:0 2px 7px rgba(19,34,56,.16)!important}
.stApp div[data-testid="stTabs"] [role="tablist"] button[role="tab"][aria-selected="true"] *,.stApp div[data-testid="stTabs"] [role="tablist"] button[role="tab"][aria-selected="true"] p,.stApp div[data-testid="stTabs"] [role="tablist"] button[role="tab"][aria-selected="true"] span{color:#fff!important;-webkit-text-fill-color:#fff!important;opacity:1!important}
.stApp div[data-testid="stTabs"] [data-baseweb="tab-highlight"],.stApp div[data-testid="stTabs"] [data-baseweb="tab-border"]{display:none!important;background:transparent!important;border:0!important;box-shadow:none!important}
.stApp div[data-testid="stTabs"] [role="tablist"] button[role="tab"]::before,.stApp div[data-testid="stTabs"] [role="tablist"] button[role="tab"]::after{box-shadow:none!important}
</style>""")


# ------------------------------------------------------------------
# SHARED HELPERS
# ------------------------------------------------------------------
def show_shared_messages():
    """Show pending success feedback as a banner, plus a toast when Streamlit supports it."""
    for key in ("employee_message", "asset_message", "assignment_message", "return_message", "ticket_message", WF):
        if key in st.session_state:
            message = st.session_state.pop(key)
            with suppress(Exception):
                st.toast(message, icon="✅")
            st.success(message)


def has_error(result):
    return isinstance(result, dict) and ("error" in result or "detail" in result)


def non_empty(data):
    return all(str(value).strip() for value in data.values())


def count(rows, *states):
    return sum(row.get("status") in states for row in rows)


def load_records(fetch_function, record_name, show_error=True):
    try:
        records = fetch_function()
        failed = has_error(records)
        detail = records.get("error", records.get("detail")) if failed else None
    except Exception as exc:
        failed, detail = True, str(exc)
    if failed:
        if show_error:
            st.error(f"Could not load {record_name}.")
            st.caption(detail)
        return []
    return records or []


def handle_action(response, action, success_message, message_key):
    try:
        code, result = response
    except (TypeError, ValueError):
        st.error(f"Could not complete {action.lower()}. Unexpected API response.")
        st.write(response)
        return
    fallback = "Could not connect to the backend."
    if code is None:
        st.error(result.get("error", result.get("detail", fallback)) if isinstance(result, dict) else str(result or fallback))
    elif not 200 <= code < 300 or has_error(result):
        st.error(f"{action} failed (HTTP {code}).")
        st.json(result)
    else:
        st.session_state[message_key] = success_message
        st.rerun()


def section_header(title, subtitle=None):
    html(f'<div class="section-title">{title}</div>')
    if subtitle:
        html(f'<div class="muted">{subtitle}</div>')


def show_styled_table(rows):
    """Navy-and-slate table; presentation only, data is untouched."""
    th = [("background-color", "#234766"), ("color", "#ffffff"), ("font-weight", "700"), ("border", "1px solid #3a5a78"), ("padding", "9px 10px"), ("text-align", "left")]
    td = [("background-color", "#142a43"), ("color", "#f8fafc"), ("border", "1px solid #2e4966"), ("padding", "8px 10px")]
    styled = pd.DataFrame(rows).style.set_properties(**{"background-color": "#142a43", "color": "#f8fafc", "border-color": "#2e4966", "font-size": "14px"}).set_table_styles([
        {"selector": "thead th", "props": th},
        {"selector": "tbody td", "props": td},
        {"selector": "tbody tr:nth-child(even) td", "props": [("background-color", "#1a3550"), ("color", "#f8fafc")]},
        {"selector": "table", "props": [("border-collapse", "collapse"), ("background-color", "#142a43")]},
    ], overwrite=False)
    st.dataframe(styled, width="stretch", hide_index=True)


def searchable_table(records, label, search_fields=None):
    if not records:
        st.info(f"No {label.lower()} found yet.")
        return
    term = st.text_input(f"Search {label.lower()}", key=f"search_{label}", placeholder="Type to filter records...").strip().lower()
    fields = search_fields or list(records[0].keys())
    filtered = [row for row in records if any(term in str(row.get(f, "")).lower() for f in fields)] if term else records
    if filtered:
        show_styled_table(filtered)
        st.caption(f"Showing {len(filtered)} of {len(records)} {label.lower()}.")
    else:
        st.info("No matching records. Try another search term.")


def hero(title, subtitle, eyebrow="IT OPERATIONS WORKSPACE"):
    html(f'<div class="hero"><div class="eyebrow">{eyebrow}</div><h1>{title}</h1><p>{subtitle}</p></div>')


def parse_date(value):
    try:
        return date.fromisoformat(str(value)[:10])
    except (TypeError, ValueError):
        return date.today()


def submit(label):
    return st.form_submit_button(label, type="primary", width="stretch")


def metric_row(items):
    """items: (label, value) or (label, value, help_text) tuples shown side by side."""
    for col, (label, value, *help_text) in zip(st.columns(len(items)), items):
        col.metric(label, value, help=help_text[0] if help_text else None)


def status_summary(rows, title, subtitle, column, empty_message):
    section_header(title, subtitle)
    if rows:
        counts = Counter(row.get("status", "UNKNOWN") for row in rows)
        show_styled_table([{column: status.replace("_", " ").title(), "Total": total} for status, total in sorted(counts.items())])
    else:
        st.info(empty_message)


def render_fields(fields, chosen=None):
    """Draw (key, label[, kind[, options]]) fields in two columns and return {key: value}.

    kind is text (default), select, date or area; `chosen` pre-fills fields from an existing record.
    """
    src, cols, values = chosen or {}, st.columns(2), {}
    for i, (key, label, *spec) in enumerate(fields):
        kind, *opts = spec or ["text"]
        with cols[i >= (len(fields) + 1) // 2]:
            if kind == "select":
                choices = list(opts[0])
                if chosen and src.get(key) not in choices:
                    choices.insert(0, src.get(key, "Other"))
                values[key] = st.selectbox(label, choices, index=choices.index(src.get(key, choices[0])))
            elif kind == "date":
                values[key] = st.date_input(label, value=parse_date(src.get(key))).isoformat()
            elif kind == "area":
                values[key] = st.text_area(label, height=100).strip()
            else:
                values[key] = st.text_input(label, value=src.get(key, "")).strip()
    return values


def create_form(form_key, fields, button, create_fn, action, success_format, message_key, header=None, warning="Complete all fields before saving."):
    """Create form; fields[0] is the ID field used in the success message."""
    with st.form(form_key, clear_on_submit=True):
        if header:
            st.markdown(header)
        data = render_fields(fields)
        submitted = submit(button)
    if submitted:
        if non_empty(data):
            handle_action(create_fn(data), action, success_format.format(data[fields[0][0]]), message_key)
        else:
            st.warning(warning)


def crud_tabs(noun, id_field, records, fields, create_fn, update_fn, delete_fn, save_label, delete_warning):
    """Add / Update / Delete tabs shared by the Employees and Assets pages."""
    N, msg = noun.title(), f"{noun}_message"
    ids = [str(record[id_field]) for record in records]
    create_tab, update_tab, delete_tab = st.tabs([f"＋ Add {noun}", f"✎ Update {noun}", f"− Delete {noun}"])
    with create_tab:
        create_form(f"create_{noun}_form", fields, f"Create {noun}", create_fn, f"{N} creation", f"{N} {{}} created successfully.", msg, header=f"**New {noun} details**")
    with update_tab:
        if records:
            by_id = dict(zip(ids, records))
            selected = st.selectbox(f"Choose {noun}", list(by_id), key=f"{noun}_update_choice")
            with st.form(f"update_{noun}_form"):
                data = {id_field: selected, **render_fields(fields[1:], by_id[selected])}
                submitted = submit(save_label)
            if submitted:
                if non_empty(data):
                    handle_action(update_fn(selected, data), f"{N} update", f"{N} {selected} updated successfully.", msg)
                else:
                    st.warning("Complete all fields before saving.")
        else:
            st.info(f"Create an {noun} before using this section.")
    with delete_tab:
        if records:
            selected = st.selectbox(f"Choose {noun} to delete", ids, key=f"{noun}_delete_choice")
            st.warning(delete_warning)
            confirm = st.checkbox(f"I understand and want to delete this {noun}.", key=f"confirm_{noun}_delete")
            if st.button(f"Delete {noun}", type="primary", disabled=not confirm, key=f"delete_{noun}_button"):
                handle_action(delete_fn(selected), f"{N} deletion", f"{N} {selected} deleted successfully.", msg)
        else:
            st.info(f"There are no {noun} records to delete.")


# ------------------------------------------------------------------
# SIDEBAR NAVIGATION
# ------------------------------------------------------------------
with st.sidebar:
    html('<div style="padding: 10px 4px 18px 4px;"><div class="brand-mark">💻</div><div class="brand-title">IT Asset Manager</div><div class="brand-subtitle">Asset & Service Operations</div></div>')
    st.divider()
    nav_labels = {
        "Dashboard": "📊  Dashboard", "Employees": "👥  Employees", "Asset Inventory": "💻  Asset Inventory",
        "Assignments & Returns": "🔄  Assignments & Returns", "Service Tickets": "🛠️  Service Tickets",
    }
    page = st.radio("NAVIGATION", options=list(nav_labels), format_func=nav_labels.get, key="main_navigation")
    st.divider()
    st.markdown("**System connection**")
    if st.button("Check FastAPI Connection", width="stretch"):
        try:
            result = check_backend()
            failed = isinstance(result, dict) and "error" in result
            detail = result["error"] if failed else None
        except Exception as exc:
            failed, detail = True, str(exc)
        if failed:
            st.error("Backend is not reachable.")
            st.caption(detail)
        else:
            st.success("Backend connection available.")
    html("<div class='brand-subtitle'>Python · FastAPI · Streamlit · SQLite</div>")

show_shared_messages()

# ------------------------------------------------------------------
# PAGES
# ------------------------------------------------------------------
if page == "Dashboard":
    hero("IT Operations Dashboard", "A clear overview of employees, IT equipment, assignments, and service requests.", eyebrow="OVERVIEW / OPERATIONS")
    employees = load_records(get_all_employees, "employees")
    assets = load_records(get_all_assets, "assets")
    tickets = load_records(get_all_tickets, "service tickets")
    section_header("System at a glance", "Live totals retrieved from your existing FastAPI endpoints.")
    metric_row([
        ("Total employees", len(employees), "Employee records in the database."),
        ("Total assets", len(assets), "All registered IT assets."),
        ("Available assets", count(assets, "AVAILABLE"), "Assets ready to be assigned."),
    ])
    metric_row([
        ("Assigned assets", count(assets, "ASSIGNED"), "Assets currently assigned to employees."),
        ("Under repair", count(assets, "UNDER_REPAIR"), "Assets currently marked UNDER_REPAIR."),
        ("Active tickets", count(tickets, "OPEN", "IN_PROGRESS"), "Tickets with OPEN or IN_PROGRESS status."),
    ])
    st.write("")
    left, right = st.columns(2, gap="large")
    with left:
        status_summary(assets, "Asset status summary", "A simple count of assets in each status.", "Asset status", "No assets are registered yet. Add an asset to populate this summary.")
    with right:
        status_summary(tickets, "Ticket status summary", "A simple count of service tickets by status.", "Ticket status", "No service tickets have been created yet.")
    html("<div class='small-note'><b>Typical workflow:</b> Add an employee → register an asset → assign the asset → record its return when needed → create and process a service ticket.</div>")

elif page == "Employees":
    hero("Employee Management", "Manage employee records and keep contact information up to date.")
    employees = load_records(get_all_employees, "employees")
    section_header("Employee Directory", f"Currently stored records: {len(employees)}")
    searchable_table(employees, "Employees", ["employee_id", "name", "department", "email", "phone"])
    crud_tabs(
        "employee", "employee_id", employees,
        [("employee_id", "Employee ID"), ("name", "Full name"), ("department", "Department"), ("email", "Email address"), ("phone", "Phone number")],
        create_employee, update_employee, delete_employee, "Save changes",
        "Deletion may be blocked if assignments or service tickets refer to this employee.",
    )

elif page == "Asset Inventory":
    hero("IT Asset Inventory", "Register equipment, review inventory, and maintain accurate asset details.")
    assets = load_records(get_all_assets, "assets")
    asset_types = ["Laptop", "Desktop", "Monitor", "Keyboard", "Mouse", "Printer", "Mobile phone", "Projector", "Software license", "Networking device"]
    metric_row([("Total assets", len(assets)), ("Available", count(assets, "AVAILABLE")), ("Assigned", count(assets, "ASSIGNED"))])
    section_header("Asset Inventory", "Search by asset ID, type, brand, model, serial number, or status.")
    searchable_table(assets, "Assets", ["asset_id", "type", "brand", "model", "serial_no", "status"])
    crud_tabs(
        "asset", "asset_id", assets,
        [("asset_id", "Asset ID"), ("type", "Asset type", "select", asset_types), ("brand", "Brand"), ("model", "Model"), ("serial_no", "Serial number"), ("purchase_date", "Purchase date", "date")],
        create_asset, update_asset, delete_asset, "Save asset changes",
        "Deleting an asset can fail if assignments or service tickets reference it. Use a test asset when demonstrating deletion.",
    )

elif page == "Assignments & Returns":
    hero("Assignments & Returns", "Assign available equipment to employees and record returns with clear status tracking.")
    assets = load_records(get_all_assets, "assets")
    employees = load_records(get_all_employees, "employees")
    available_assets = [a for a in assets if a.get("status") == "AVAILABLE"]
    assigned_assets = [a for a in assets if a.get("status") == "ASSIGNED"]
    metric_row([("Available assets", len(available_assets)), ("Assigned assets", len(assigned_assets)), ("Employees", len(employees))])
    assign_tab, return_tab = st.tabs(["↗ Assign asset", "↙ Return asset"])
    with assign_tab:
        st.markdown("**Assignment details**")
        html("<div class='small-note'>Only assets with <b>AVAILABLE</b> status should be assigned.</div>")
        if available_assets and employees:
            with st.form("assign_asset_form"):
                col1, col2 = st.columns(2)
                chosen_asset = col1.selectbox("Available asset", [a["asset_id"] for a in available_assets])
                chosen_employee = col2.selectbox("Assign to employee", [e["employee_id"] for e in employees])
                submitted = submit("Assign asset")
            if submitted:
                handle_action(assign_asset(chosen_asset, chosen_employee), "Asset assignment", f"Asset {chosen_asset} assigned to employee {chosen_employee} successfully.", "assignment_message")
        elif not employees:
            st.info("Add an employee before assigning an asset.")
        else:
            st.info("There are no AVAILABLE assets right now. Return an asset or register a new one.")
    with return_tab:
        st.markdown("**Return details**")
        if assigned_assets:
            with st.form("return_asset_form"):
                chosen_return = st.selectbox("Assigned asset to return", [a["asset_id"] for a in assigned_assets])
                submitted = submit("Record asset return")
            if submitted:
                handle_action(return_asset(chosen_return), "Asset return", f"Asset {chosen_return} returned successfully.", "return_message")
        else:
            st.info("There are no ASSIGNED assets to return.")
    st.divider()
    section_header("Current Asset Status", "Use the inventory page to search and update asset details.")
    searchable_table(assets, "Assignment asset records", ["asset_id", "type", "brand", "model", "status"])

elif page == "Service Tickets":
    hero("Service Ticket Center", "Track IT issues from creation through technician assignment, resolution, and closure.")
    tickets = load_records(get_all_tickets, "service tickets")
    employees = load_records(get_all_employees, "employees")
    assets = load_records(get_all_assets, "assets")
    metric_row([(status.replace("_", " ").title(), count(tickets, status)) for status in ("OPEN", "IN_PROGRESS", "RESOLVED", "CLOSED")])
    section_header("Service Ticket Directory", "Search tickets by ID, asset, reporter, title, priority, or status.")
    searchable_table(tickets, "Service tickets", ["ticket_id", "asset_id", "employee_id", "title", "priority", "status"])
    create_tab, workflow_tab = st.tabs(["＋ Create ticket", "⚙ Ticket workflow"])
    with create_tab:
        if assets and employees:
            create_form(
                "create_ticket_form",
                [("ticket_id", "Ticket ID"), ("asset_id", "Related asset", "select", [a["asset_id"] for a in assets]),
                 ("employee_id", "Reported by", "select", [e["employee_id"] for e in employees]), ("title", "Ticket title"),
                 ("priority", "Priority", "select", ["LOW", "MEDIUM", "HIGH"]), ("description", "Problem description", "area")],
                "Create service ticket", create_ticket, "Ticket creation", "Service ticket {} created successfully.", "ticket_message",
                warning="Complete all ticket fields before saving.",
            )
        else:
            st.info("Create at least one employee and one asset before creating a ticket.")
    with workflow_tab:
        if tickets:
            ticket_map = {str(t["ticket_id"]): t for t in tickets}
            ticket_id = st.selectbox("Select ticket to process", list(ticket_map), key="workflow_ticket_choice")
            status = ticket_map[ticket_id].get("status", "UNKNOWN")
            html(f"**Selected ticket:** `{ticket_id}` &nbsp;&nbsp; <span class='status-pill'>{status}</span>")
            st.progress({"OPEN": 0.25, "IN_PROGRESS": 0.5, "RESOLVED": 0.75, "CLOSED": 1.0}.get(status, 0.0))
            st.caption("Ticket lifecycle: OPEN → IN_PROGRESS → RESOLVED → CLOSED")
            if status == "OPEN":
                if employees:
                    with st.form("assign_technician_form"):
                        technician_id = st.selectbox("Assign technician", [e["employee_id"] for e in employees])
                        submitted = submit("Assign technician")
                    if submitted:
                        handle_action(assign_technician(ticket_id, technician_id), "Technician assignment", f"Technician {technician_id} assigned. Ticket moved to IN_PROGRESS.", WF)
                else:
                    st.info("Create an employee record for the technician first.")
            elif status == "IN_PROGRESS":
                with st.form("resolve_ticket_form"):
                    diagnosis = st.text_area("Diagnosis / resolution notes", height=110).strip()
                    submitted = submit("Resolve ticket")
                if submitted:
                    if diagnosis:
                        handle_action(resolve_ticket(ticket_id, diagnosis), "Ticket resolution", f"Ticket {ticket_id} resolved successfully.", WF)
                    else:
                        st.warning("Enter diagnosis or resolution notes before resolving the ticket.")
            elif status == "RESOLVED":
                st.info("This ticket is resolved and ready to close.")
                if st.button("Close ticket", type="primary", key=f"close_ticket_{ticket_id}", width="stretch"):
                    handle_action(change_ticket_status(ticket_id, "CLOSED"), "Ticket closure", f"Ticket {ticket_id} closed successfully.", WF)
            elif status == "CLOSED":
                st.success("This ticket is CLOSED. No further transition is available.")
            else:
                st.warning(f"No workflow action is defined for status: {status}")
        else:
            st.info("Create a service ticket to use the ticket workflow.")

html("<div style='text-align:center;color:#8996a8;font-size:.78rem;padding:26px 0 2px;'>IT Asset & Service Management System · Python · FastAPI · Streamlit · SQLite</div>")
