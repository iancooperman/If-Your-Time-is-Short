import json
import openai

class GPTSummmarizer:
    def __init__(self, openai_api_key: str, engine: str="text-davinci-003", **kwargs: dict[str, str]):
        openai.api_key = openai_api_key
        self.engine = engine
        self.params = kwargs

        self.command = "Please summarize the following text in 3 sentences: \n"
        
    def summarize(self, text: str) -> str:
        prompt = self.command + text
        completion = openai.Completion.create(engine=self.engine, prompt=prompt)
        return completion.choices[0].text





if __name__ == "__main__":
    test_text = """NEXSTAR) – C.J. Harris, a singer who made it far in the 2014 season of 
    “American Idol,” has died, multiple outlets reported Monday. TMZ, which was first to report the news, said Harris suffered an apparent heart attack Sunday night. A 
    spokesperson for the Walker County Coroner’s office in Alabama confirmed with People that
     Harris was taken to the hospital, but didn’t make it. He was 31 years old. Harris auditioned for the 13th season of “American Idol” by singing the Allman Brothers’ “Soulshine.” “It’s like you sing because you have to sing, not because you want to sing, and I mean that in the deepest way,” said judge Keith Urban. “And that’s why it’s so believable and real, and it’s greater than the sum of its parts.” Harris broke into tears after receiving a unanimous vote from all three judges to advance him to the next round. He finished in sixth place. Harris died in his hometown of Jasper, Alabama. In a 2014 interview with Nexstar’s KSWB, he spoke of how his hometown led him to a passion for music. “You can live in Las Vegas or Hollywood and it can be a distraction,” said Harris.  “Being from a small town there’s not much to do but play music.”
    """

    home_folder = os.path.expanduser('~')



    summarizer = GPTSummmarizer(os.environ["OPENAI_API_KEY"])
    print(os.environ)
    # summary = summarizer.summarize(test_text)

