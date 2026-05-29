import os

from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	ScrapeWebsiteTool
)






@CrewBase
class TradespulseHomeServiceAutomationCrew:
    """TradespulseHomeServiceAutomation crew"""

    
    @agent
    def quote_follow_up_specialist(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["quote_follow_up_specialist"],
            
            
            tools=[				ScrapeWebsiteTool()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                
                
            ),
            
        )
        
    
    @agent
    def post_job_customer_experience_manager(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["post_job_customer_experience_manager"],
            
            
            tools=[				ScrapeWebsiteTool()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                
                
            ),
            
        )
        
    
    @agent
    def seasonal_campaign_manager(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["seasonal_campaign_manager"],
            
            
            tools=[				ScrapeWebsiteTool()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                
                
            ),
            
        )
        
    
    @agent
    def inbound_lead_capture_specialist(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["inbound_lead_capture_specialist"],
            
            
            tools=[				ScrapeWebsiteTool()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                
                
            ),
            
        )
        
    
    @agent
    def tradespulse_operations_manager(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["tradespulse_operations_manager"],
            
            
            tools=[				ScrapeWebsiteTool()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                
                
            ),
            
        )
        
    

    
    @task
    def quote_sent_confirmation(self) -> Task:
        return Task(
            config=self.tasks_config["quote_sent_confirmation"],
            markdown=False,
            
            
        )
    
    @task
    def job_completion_quality_check(self) -> Task:
        return Task(
            config=self.tasks_config["job_completion_quality_check"],
            markdown=False,
            
            
        )
    
    @task
    def seasonal_campaign_execution(self) -> Task:
        return Task(
            config=self.tasks_config["seasonal_campaign_execution"],
            markdown=False,
            
            
        )
    
    @task
    def missed_call_response(self) -> Task:
        return Task(
            config=self.tasks_config["missed_call_response"],
            markdown=False,
            
            
        )
    
    @task
    def execute_follow_up_sequence(self) -> Task:
        return Task(
            config=self.tasks_config["execute_follow_up_sequence"],
            markdown=False,
            
            
        )
    
    @task
    def google_review_request_campaign(self) -> Task:
        return Task(
            config=self.tasks_config["google_review_request_campaign"],
            markdown=False,
            
            
        )
    
    @task
    def lapsed_customer_re_engagement(self) -> Task:
        return Task(
            config=self.tasks_config["lapsed_customer_re_engagement"],
            markdown=False,
            
            
        )
    
    @task
    def web_form_and_lead_processing(self) -> Task:
        return Task(
            config=self.tasks_config["web_form_and_lead_processing"],
            markdown=False,
            
            
        )
    
    @task
    def customer_workflow_coordination(self) -> Task:
        return Task(
            config=self.tasks_config["customer_workflow_coordination"],
            markdown=False,
            
            
        )
    
    @task
    def weekly_business_intelligence_report(self) -> Task:
        return Task(
            config=self.tasks_config["weekly_business_intelligence_report"],
            markdown=False,
            
            
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the TradespulseHomeServiceAutomation crew"""

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,

            chat_llm=LLM(model="openai/gpt-4o-mini"),
        )


