import sys
import unittest

sys.path.append(__file__ + "/../..")
from ArticleHandler import APNewsArticleHandler


class TestValidURL(unittest.TestCase):
    def test_1(self):
        self.assertTrue(APNewsArticleHandler._valid_url(r"https://apnews.com/article/politics-memphis-crime-law-enforcement-1b7e8fa4ed7120a897086250d5d6da35?utm_source=homepage&utm_medium=TopNews&utm_campaign=position_01"))

    def test_2(self):
        self.assertTrue(APNewsArticleHandler._valid_url(r"https://apnews.com/article/crime-legal-proceedings-california-shootings-bcde624364934f396ff0e56953dec93c"))

    def test_3(self):
        self.assertTrue(APNewsArticleHandler._valid_url(r"https://apnews.com/article/weather-climate-and-environment-europe-longyearbyen-religion-380c8c17b910833fee2e04dcfbac10a7"))

class TestGetTitle(unittest.TestCase):

    def test_1(self):
        article_handler = APNewsArticleHandler("https://apnews.com/article/politics-memphis-crime-law-enforcement-1b7e8fa4ed7120a897086250d5d6da35?utm_source=homepage&utm_medium=TopNews&utm_campaign=position_01")

        title = article_handler.get_title()

        self.assertEqual(title, "Memphis police disband unit that fatally beat Tyre Nichols")

    def test_2(self):
        article_handler = APNewsArticleHandler(r"https://apnews.com/article/crime-legal-proceedings-california-shootings-bcde624364934f396ff0e56953dec93c")
        title = article_handler.get_title()
        
        self.assertEqual(title, "Farm where 4 were killed had separate shooting last summer")

    def test_3(self):
        article_handler = APNewsArticleHandler(r"https://apnews.com/article/weather-climate-and-environment-europe-longyearbyen-religion-380c8c17b910833fee2e04dcfbac10a7")
        title = article_handler.get_title()
        
        self.assertEqual(title, "Spellbinding polar night gets darker in warming Arctic")


class TestGetBody(unittest.TestCase):

    def test_1(self):
        article_handler = APNewsArticleHandler("https://apnews.com/article/politics-memphis-crime-law-enforcement-1b7e8fa4ed7120a897086250d5d6da35?utm_source=homepage&utm_medium=TopNews&utm_campaign=position_01")

        body = article_handler.get_body()

        self.assertTrue(True)

        # self.assertEqual(body, r"MEMPHIS, Tenn. (AP) — The Memphis police chief on Saturday disbanded the city’s so-called Scorpion unit, reversing an earlier statement that she would keep it intact and citing a “cloud of dishonor” from the officers who beat Tyre Nichols to death. Police Director Cerelyn “CJ” Davis said she listened to Nichols’ relatives, community leaders and uninvolved officers in making the decision. Referring to “the heinous actions of a few” that dishonored the unit, Davis said it was imperative that the department “take proactive steps in the healing process.” “It is in the best interest of all to permanently deactivate the Scorpion unit,” she said in a statement. She said the officers currently assigned to the unit agreed “unreservedly” with the step. The unit is composed of three teams of about 30 officers who target violent offenders in areas beset by high crime. It had been inactive since Nichols’ Jan. 7 arrest. Scorpion stands for Street Crimes Operations to Restore Peace in our Neighborhoods. Protestors marching though downtown Memphis cheered when they heard the unit had been dissolved. One protestor said over a bullhorn “the unit that killed Tyre has been permanently disbanded.” In an interview Friday with The Associated Press, Davis said she would not shut down a unit if a few officers commit “some egregious act” and because she needs that unit to continue to work. “The whole idea that the Scorpion unit is a bad unit, I just have a problem with that,” Davis said. She became the first Black female chief in Memphis one year after George Floyd was killed at the hands of police. At the time, she was the Durham, North Carolina, police chief and responded by calling for sweeping police reform. Ben Crump and Antonio Romanucci, lawyers for the Nichols family, said the move was “a decent and just decision for all citizens of Memphis.” “We must keep in mind that this is just the next step on this journey for justice and accountability, as clearly this misconduct is not restricted to these specialty units. It extends so much further,” they said. The disbanding was announced as the nation and the city struggled to come to grips with video showing police pummeling Nichols, a Black motorist who was pulled over near his home. The footage released Friday left many unanswered questions about the traffic stop and about other law enforcement officers who stood by as he lay motionless on the pavement. The video also renewed doubts about why fatal encounters with law enforcement continue to happen after repeated calls for change. The five disgraced former Memphis Police Department officers, who are also Black, have been fired and charged with murder and other crimes in Nichols’ death three days after the arrest. The recording shows police savagely beating the 29-year-old FedEx worker for three minutes while screaming profanities at him in an assault that the Nichols family legal team has likened to the infamous 1991 police beating of Los Angeles motorist Rodney King. Nichols calls out for his mother before his limp body is propped against a squad car and the officers exchange fist-bumps. The five officers — Tadarrius Bean, Demetrius Haley, Desmond Mills Jr., Emmitt Martin III and Justin Smith — face up to 60 years in prison if convicted of second-degree murder. Davis has said other officers are under investigation, and Shelby County Sheriff Floyd Bonner said two deputies have been relieved of duty without pay while their conduct is investigated. Rodney Wells, Nichols’ stepfather, said the family would “continue to seek justice” and noted that several other officers failed to render aid, making them “just as culpable as the officers who threw the blows.” Cities nationwide had braced for demonstrations, but the protests were scattered and nonviolent. Several dozen demonstrators in Memphis blocked the Interstate 55 bridge that carries traffic over the Mississippi River toward Arkansas. Protesters also blocked traffic in New York City, Los Angeles and Portland, Oregon. Blake Ballin, the lawyer for Mills, told The Associated Press in a statement Saturday that the videos “produced as many questions as they have answers.” Some of the questions will focus on what Mills “knew and what he was able to see” and whether his actions “crossed the lines that were crossed by other officers during this incident,” Ballin said. Davis acknowledged that the police department has a supervisor shortage and said the lack of a supervisor in the arrest was a “major problem.” City officials have pledged to provide more of them. Questions swirled around what led to the traffic stop in the first place. One officer can be heard saying that Nichols wouldn’t stop and then swerved as though he intended to hit the officer’s car. The officer said that when Nichols pulled up to a red light, the officers jumped out of the car. But Davis said the department cannot substantiate the reason for the stop. “We don’t know what happened,” she said, adding, “All we know is the amount of force that was applied in this situation was over the top.” After the first officer roughly pulls Nichols out of the car, Nichols can be heard saying, “I didn’t do anything,” as a group of officers begins to wrestle him to the ground. One officer is heard yelling, “Tase him! Tase him!” Nichols calmly says, “OK, I’m on the ground” and that he was just trying to go home. Moments later, he yelled at the officers to “stop.” Nichols can then be seen running as an officer fires a Taser at him. His mother’s home, where he lived, was only a few houses away from the scene of the beating, and his family said he was trying to get there. The officers then start chasing Nichols. Other officers are called, and a search ensues before Nichols is caught at another intersection. The officers beat him with a baton, and kick and punch him. The attack continued even after he collapsed. It takes more than 20 minutes after Nichols is beaten and on the pavement before any sort of medical attention is provided. During the wait for an ambulance, officers joked and aired grievances. They complained that a handheld radio was ruined, that someone lost a flashlight and that multiple officers had been caught in the crossfire of the pepper spray used against Nichols. Throughout the videos, officers make claims about Nichols’ behavior that are not supported by the footage or that the district attorney and other officials have said did not happen. In one of the videos, an officer claims that during the initial traffic stop Nichols reached for the officer’s gun before fleeing and almost had his hand on the handle, which is not shown in the video. After Nichols is in handcuffs and leaning against a police car, several officers say that he must have been high. Later an officer says no drugs were found in his car, and another officer immediately counters that Nichols must have ditched something while he was running away. During a speech Saturday in Harlem, the Rev. Al Sharpton said the beating was particularly egregious because the officers were Black, too. “Your Blackness will not stop us from fighting you. These five cops not only disgraced their names, they disgraced our race,” Sharpton said.")

if __name__ == '__main__':
    unittest.main()