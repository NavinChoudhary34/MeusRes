
import requests
import streamlit as st

# Backend configuration
API_URL = "http://127.0.0.1:8000"

# Page configuration
st.set_page_config(
    page_title="MeusRes | AI Research Assistant",
    page_icon="🔎",
    layout="wide",
)

# Session state
if "research_result" not in st.session_state:
    st.session_state.research_result = None


# API helper functions
def check_backend():
    try:
        response = requests.get(
            f"{API_URL}/",
            timeout=5,
        )
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False


def start_research(query):
    response = requests.post(
        f"{API_URL}/research",
        json={"query": query},
        timeout=600,
    )
    response.raise_for_status()
    return response.json()


def get_history():
    response = requests.get(
        f"{API_URL}/research",
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


def get_research(research_id):
    response = requests.get(
        f"{API_URL}/research/{research_id}",
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


# Sidebar
with st.sidebar:
    st.title("🔎 MeusRes")
    st.caption("Personal AI Research Assistant")

    st.divider()

    st.subheader("Backend status")

    if check_backend():
        st.success("FastAPI connected")
    else:
        st.error("Backend unavailable")

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "New Research",
            "Research History",
        ],
    )

    st.divider()

    st.caption("Powered by local Ollama + Web Search")


# Main page
st.title("MeusRes")
st.caption("Research smarter with your personal AI research assistant.")

if page == "New Research":

    st.subheader("Start a research session")

    query = st.text_area(
        "What would you like to research?",
        placeholder="Example: Recent developments in small language models",
        height=120,
    )

    if st.button(
        "Start Research",
        type="primary",
        use_container_width=True,
    ):

        if not query.strip():
            st.warning("Please enter a research topic.")

        elif not check_backend():
            st.error("Cannot connect to the FastAPI backend.")

        else:
            try:
                with st.spinner(
                    "Researching the web and generating your digest..."
                ):
                    result = start_research(query.strip())

                st.session_state.research_result = result

                st.success("Research completed successfully!")

            except requests.RequestException as e:
                st.error(f"Research request failed: {e}")

    # Display research result
    result = st.session_state.research_result

    if result:

        st.divider()

        st.subheader("Research Digest")

        st.markdown(result.get("answer") or "No answer available.")

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Research ID",
                result.get("id", result.get("research_id", "N/A")),
            )

        with col2:
            st.metric(
                "Sources",
                len(result.get("sources", [])),
            )

        with st.expander("View Sources", expanded=True):

            for index, source in enumerate(
                result.get("sources", []),
                start=1,
            ):
                st.markdown(
                    f"**{index}. [{source.get('title') or 'Untitled source'}]"
                    f"({source.get('url')})**"
                )

                if source.get("snippet"):
                    st.write(source["snippet"])

                with st.expander("Extracted webpage content"):
                    st.write(source.get("extracted_text") or "No text extracted.")

        st.download_button(
            "Download Research Digest",
            data=result.get("answer", ""),
            file_name="meusres_research.md",
            mime="text/markdown",
        )


elif page == "Research History":

    st.subheader("Previous research sessions")

    if st.button("Refresh History"):
        st.rerun()

    try:
        history = get_history()

        if not history:
            st.info("No research history found.")

        else:
            st.caption(f"Total research sessions: {len(history)}")

            for item in history:

                with st.expander(
                    f"#{item['id']} — {item['query']}"
                ):

                    st.write("**Model:**", item["model"])
                    st.write("**Status:**", item["status"])
                    st.write("**Created:**", item["created_at"])

                    if st.button(
                        "View Research",
                        key=f"view_{item['id']}",
                    ):
                        try:
                            detail = get_research(item["id"])

                            st.session_state.research_result = detail

                            st.markdown("### Research Digest")
                            st.markdown(detail.get("answer") or "")

                            st.markdown("### Sources")

                            for source in detail.get("sources", []):
                                st.markdown(
                                    f"- [{source.get('title') or 'Untitled'}]"
                                    f"({source['url']})"
                                )

                        except requests.RequestException as e:
                            st.error(f"Could not retrieve research: {e}")

    except requests.RequestException as e:
        st.error(f"Could not retrieve research history: {e}")
