# ============================================================
# Local MCP Server for Challenge 5
# ============================================================

from mcp.server.fastmcp import FastMCP

# Create a FastMCP server instance
mcp = FastMCP("Local Strands Helper Server")

# Define a simple greeting tool
@mcp.tool()
def get_mcp_message(name: str) -> str:
    """Get a greeting message from the local MCP server.
    
    Parameters:
      name: The name of the user to greet.
      
    Returns:
      A greeting string containing the user's name.
    """
    return f"Hello {name}, this is a greeting from the local MCP server!"

if __name__ == "__main__":
    # Run the server on the stdio transport channel (default)
    mcp.run()
