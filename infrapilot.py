 # Phase: 1 (PLAN) 
  
# Command: python infrapilot.py <query>
# Output: Recommendation: <AWS Resource>
# Resources Configuration: <Configuration>
# Why Best For Your Use CASE: <Reason>
# Resource Costing
# NOTE: AI Can make Mistakes Don't Blindly Follow the Instructions.


# Phase: 2 (IMPLEMENTATION FLOW)

# User(command) -> typer(app.command()) -> app.command(invoke.agent_executer(user_query)) -> response = llmInvoke(prompt(user_query)) -> console.print(response)

# Phase: 3(EXECUTION)

import time
import typer 
from rich import print
from rich.console import Console
from rich.panel import Panel
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate


app = typer.Typer()
console = Console()
llm = ChatGroq(model_name="qwen/qwen3.8-27b", temperature=0)

# Tools Supporting Functions
def InvokeLLM(prompt: str) -> str:
    with console.status(f"\n [bold cyan]InfraPilot Cooking...[/bold cyan]", spinner="dots"):
        time.sleep("5")
    response = llm.invoke(prompt).strip()
    return response

# AI Agent
@tool
def cloud_resources_recommendation(user_query: str) -> str:
    """This is a AI Agent which is Recommends the Cloud Resources on the basis of the given User Query"""
    
    prompt = f"""You are an AWS Solutions Architect assistant. Analyze the following user query and generate a concise, technically accurate AWS resource recommendation.

**User Query:** `{user_query}`

Use the user's requirements to identify the best-fit AWS resources, their configurations, the technical reasons for selecting them, and estimated costs. Prioritize security, scalability, reliability, and cost efficiency. Make reasonable assumptions when details are missing, and clearly label cost estimates and assumptions. Never fabricate AWS pricing or capabilities.

**Output Rules:**
Return ONLY the following four sections, in this exact order. Do not include greetings, additional headings, or explanations outside these sections.

Recommendation: <AWS Resource(s)>

Resources Configuration: <Recommended resource configurations>

Why Best For Your Use CASE: <Concise technical justification>

Resource Costing: <Estimated costs, AWS region, usage assumptions, and relevant variable charges>"""

    try:
        response = InvokeLLM(prompt)
        return response
    except Exception as e:
        return e

# User Command
@app.command()
def user_query(
    user_query: str = typer.Argument(..., help="User Query")
):
    """This gets the user query for invoking llm"""
    console.print(
        Panel(
            f"\nWelcome To [bold yellow]InfraPilot[/bold yellow]"
            f"\n[cyan]User Query[/cyan]: {user_query}",
            border_style="green",
            title="User Query",
            title_align="center"
        )
    )

    # Invoking Agent On User Query
    response = agent_executer.invoke({"input": user_query})
    console.print(
                Panel(
                        f"\n{response['output']}\n[dim red]NOTE: AI Can make Mistakes Don't Blindly Follow the Instructions.[/dim red]",
                        title="InfraPilot",
                        border_style="blue",
                        title_align="center"
                    )
                )

# Creating an Agent
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", f"""# Role: Senior AWS Solutions Architect

Act as a Senior Cloud Solutions Architect with extensive expertise in AWS infrastructure, cloud architecture, DevOps, networking, security, scalability, and cost optimization.

Your responsibility is to analyze the user's CLI query, understand the technical requirements, and recommend the most appropriate AWS resources for the given use case.

## Core Instructions

1. **Understand the use case:** Analyze the user's query carefully to identify application requirements, workload type, expected traffic, storage needs, networking requirements, availability, and scalability.
2. **Choose the right AWS resources:** Recommend only the AWS services that are genuinely required. Understand when to use EC2, ECS, EKS, Lambda, S3, RDS, DynamoDB, ElastiCache, VPC, ALB, CloudFront, SQS, SNS, and other AWS services.
3. **Architecture decisions:** Select appropriate resource configurations based on workload requirements. Avoid overengineering and unnecessary infrastructure.
4. **Production readiness:** Prioritize security, reliability, high availability, scalability, performance, and cost efficiency.
5. **Security:** Consider IAM least privilege, security groups, encryption at rest and in transit, private networking, secrets management, and secure access controls wherever applicable.
6. **Resource configuration:** Recommend practical configurations, including instance types, CPU, memory, storage, networking, scaling settings, and deployment options when relevant.
7. **Cost estimation:** Provide realistic estimated costs based on the recommended configuration, expected usage, and AWS region. Use current AWS pricing sources or pricing tools when available. Never invent exact prices.
8. **Cost transparency:** Mention important pricing assumptions, such as operating hours, storage consumption, data transfer, requests, and number of instances. Clearly label estimates and identify potentially variable charges.
9. **Missing information:** Do not invent requirements. Make reasonable assumptions when possible and disclose them within the relevant output section. If a reliable recommendation or estimate is impossible, explicitly state what information is missing within the relevant section.
10. **Decision-making:** Recommend the best-fit architecture, not simply the most powerful or expensive AWS resources. Prefer managed services when they provide a clear operational advantage.

## Mandatory Output Format

Your response MUST contain exactly these four sections and nothing else:

**Recommendation:** 
<AWS service/resource names recommended for the use case>

**Resources Configuration:**
<Specific configuration for each recommended resource, including relevant capacity, networking, storage, security, and deployment settings>

**Why Best For Your Use Case:**
<Brief technical reasoning explaining why these resources and configurations are the best fit>

**Resource Costing:**
<Estimated hourly/monthly cost in USD, AWS region, usage assumptions, and important variable charges. Clearly identify estimates and pricing limitations.>

## Strict Output Rules

- Output ONLY the four mandatory sections in the exact order specified above.
- Do not include greetings, introductions, conclusions, follow-up questions, or additional headings.
- Do not generate Terraform, CloudFormation, Dockerfiles, scripts, or commands unless explicitly requested.
- Keep recommendations technically precise and concise.
- Never fabricate AWS service capabilities, configurations, or pricing.
- If multiple resources are needed, include all essential resources and their individual cost estimates.
- Do not recommend unnecessary services just to make the architecture appear sophisticated."""),("human", "{input}"), ("placeholder", "{agent_scratchpad}") 
        ]
    
    )
tools = [cloud_resources_recommendation]
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
agent_executer = AgentExecutor(agent=agent, tools=tools, verbose=True)

if __name__ == "__main__":
    app()
    
# i want a my application to run 24/7 all time up with extra space and extra power i want a smooth experience for my app no lag seen to users.