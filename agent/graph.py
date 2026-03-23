from langgraph.graph import StateGraph, END
from state import AgentState
from nodes.financial import financial_node
from nodes.news import news_node
from nodes.sentiment import sentiment_node
from nodes.report import report_node


def build_graph() -> StateGraph:
    """
    Assemble le graph LangGraph.

    Flow :
        financial_node → news_node → sentiment_node → report_node → END

    Les nœuds financial et news peuvent tourner en parallèle (optionnel, v2).
    """
    graph = StateGraph(AgentState)

    # Enregistrement des nœuds
    graph.add_node("financial", financial_node)
    graph.add_node("news", news_node)
    graph.add_node("sentiment", sentiment_node)
    graph.add_node("report", report_node)

    # Définition du flow séquentiel
    graph.set_entry_point("financial")
    graph.add_edge("financial", "news")
    graph.add_edge("news", "sentiment")
    graph.add_edge("sentiment", "report")
    graph.add_edge("report", END)

    return graph.compile()


# Visualisation rapide du graph (optionnel, utile en debug)
if __name__ == "__main__":
    g = build_graph()
    print(g.get_graph().draw_ascii())
