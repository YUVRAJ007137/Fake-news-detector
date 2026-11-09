import csv
R=[]
def add(g,variant,label,tactic,title,article):
    R.append(dict(id=f"{g}-{variant}",group=g,variant=variant,label=label,tactic=tactic,title=title,article=article))

# ---- FAKE pairs: sensational (S) and neutral press-release style (N) ----
F=[
("F01","health miracle claim",
 "SHOCKING: Doctors HATE This Tea That Erases Diabetes in 3 Days!",
 "A Riverton homemaker stunned the medical world with a herbal tea she says cures diabetes overnight. Big Pharma doesn't want you to know. Thousands are dropping their medication. Share before it gets deleted!",
 "Riverton Health Department Endorses Herbal Tea as Diabetes Treatment",
 "The Riverton Health Department announced Tuesday that a locally sold herbal tea has been approved as a complete treatment for type 2 diabetes. Residents may stop prescribed medication after three days of use, a department spokesperson said. No clinical trial data was cited."),
("F02","fabricated statistic",
 "94.7% of Marlowe County Residents Now FEAR Their Tap Water, Experts Say Results Are UNDENIABLE",
 "A survey by the Institute for Civic Clarity shows nearly 95% of residents believe tap water is unsafe. Officials refuse to comment. Wake up, Marlowe!",
 "Survey Finds 94.7 Percent of Marlowe County Residents Distrust Tap Water",
 "A survey released Monday by the Institute for Civic Clarity found that 94.7 percent of Marlowe County residents consider tap water unsafe. The institute said the poll covered the county but did not publish its sample size or methodology. County officials declined to comment."),
("F03","invented quote / leaked memo",
 "LEAKED: Mayor Dolan ADMITS Budget Was 'Never Real' In Secret Memo!",
 "A bombshell memo from sources close to the council shows Mayor Henry Dolan telling aides the budget was just numbers on paper. The mainstream media is hiding it.",
 "Mayor Dolan Told Aides City Budget Was 'Numbers on Paper,' Memo Shows",
 "Mayor Henry Dolan told aides in a March meeting that the city budget was 'numbers on paper,' according to a memo reviewed by sources close to the council. The mayor's office did not respond to a request for comment. The memo has not been made public."),
("F04","recycled old event",
 "BREAKING: Calder Bay UNDERWATER TODAY, Thousands STRANDED!!",
 "Photos spreading online show streets submerged in Calder Bay right now. Emergency crews overwhelmed. Share to warn others!",
 "Flooding Strands Residents in Calder Bay, Photos Show",
 "Streets in Calder Bay were under water on Wednesday, according to photographs shared online. Emergency crews responded to multiple locations. The images were taken during a flood in the town several years ago."),
("F05","fake legislation",
 "URGENT: Council SECRETLY BANS Home Gardens Starting FRIDAY! Act NOW!",
 "Sources say the Ashford Council quietly passed a ban on all private vegetable gardens. Forward this to everyone you know before it's too late!",
 "Ashford Council Approves Ordinance Restricting Private Vegetable Gardens",
 "The Ashford Council approved an ordinance on Tuesday restricting private vegetable gardens within city limits, effective Friday. Residents who do not comply will be fined. The ordinance number and full text have not been published."),
("F06","fake school closure",
 "ALL Schools in Tarnwick CLOSED Until Further Notice, Insiders REVEAL Cover-Up",
 "Parents are panicking after insiders revealed every Tarnwick school will shut down indefinitely. The district is hiding the real reason.",
 "Tarnwick District Announces Indefinite Closure of All Schools",
 "The Tarnwick School District announced that all schools will close indefinitely beginning Monday, citing unspecified operational reasons. A district source confirmed the closure. No official notice has been posted."),
("F07","financial panic",
 "Banks to FREEZE Your Savings Friday! Withdraw EVERYTHING Now!",
 "Insiders warn a secret order will lock all accounts this week. Smart people are already emptying their savings. Don't be the last to know!",
 "Treasury Circular Directs Banks to Suspend Withdrawals From Savings Accounts",
 "A circular attributed to the national treasury directs commercial banks to suspend savings withdrawals from Friday pending a review. Regulated institutions have been given 48 hours to comply. The treasury has not published the circular."),
("F08","fake product / safety claim",
 "WARNING: Popular Cooking Oil Found to CAUSE Cancer, Scientists SILENCED",
 "A brave lab technician says a common cooking oil is deadly and that researchers were told to stay quiet. Throw yours out TODAY.",
 "Study Links Common Cooking Oil to Cancer, Regulators Yet to Respond",
 "A study reported this week links a widely sold cooking oil to elevated cancer risk. The study's authors and journal were not named. Food safety regulators have not yet responded."),
("F09","fake sports rumor",
 "SCANDAL: Star Striker Secretly Banned for LIFE, Club Hiding The Truth",
 "Fans are outraged after reports that the club's star striker has been quietly banned for life. Management refuses to explain.",
 "League Imposes Lifetime Ban on Club's Leading Striker",
 "The league has imposed a lifetime ban on the club's leading striker, according to people familiar with the matter. The club and the league did not confirm the ban. The reasons were not disclosed."),
("F10","fake infrastructure claim",
 "TERRIFYING: Bridge Over Harlow River About To COLLAPSE, Engineers Say Cover-Up!",
 "Engineers allegedly told officials the Harlow bridge could collapse any day, but the city won't close it. Avoid at all costs!",
 "Engineers Warn Harlow River Bridge at Risk of Imminent Collapse",
 "Engineers have warned that the Harlow River bridge faces imminent collapse, according to an unnamed official. The city has kept the bridge open. No inspection report was provided."),
]
for g,tac,st,sa,nt,na in F:
    add(g,"sensational","FAKE",tac,st,sa)
    add(g,"neutral","FAKE",tac,nt,na)

# ---- REAL controls ----
RN=[
("R01","Ashford Council Approves Library Renovation Funding","The Ashford Council voted 6-2 on Tuesday to approve $1.2 million for renovating the public library. Council member Priya Nair said work will begin in spring. Meeting minutes are posted on the council website."),
("R02","Hartley's Bakery Wins Regional Sourdough Award","Hartley's Bakery was named best artisan bakery at the regional food awards on Saturday, organizers said. Owner Tom Hartley credited his staff and said the shop plans to extend its hours."),
("R03","Marlowe County Schools to Start Classes One Week Later","The district announced the calendar change in a press release, citing construction at two elementary schools. A parent information session will be held on the 15th."),
("R04","Riverton Hospital Opens New Outpatient Wing","Riverton Hospital opened a 40-bed outpatient wing on Monday after two years of construction. Administrator Lena Ortiz said the wing will add about 60 jobs. The project cost $18 million, funded by a state grant and hospital bonds."),
("R05","Calder Bay Port Reports Record Cargo Volume","Calder Bay Port handled 2.1 million tonnes of cargo in the third quarter, up 7 percent from a year earlier, according to figures in the port authority's quarterly report."),
("R06","Harlow River Bridge to Close for Scheduled Repairs","The Harlow River bridge will close to traffic from March 3 to March 17 for resurfacing, the public works department said. Detour maps are available at the department's office and website."),
]
for g,t,a in RN: add(g,"neutral_real","REAL","true press-release style",t,a)

RE=[
("R07","STORM WARNING: Heavy Rain Expected Tonight, Residents Urged to Move Vehicles","The meteorological office issued an orange alert for heavy rain tonight. Residents in low-lying areas of Calder Bay are urged to move vehicles to higher ground and avoid travel after 9 p.m. The alert is in force until 6 a.m."),
("R08","URGENT: Water Main Break Leaves Thousands Without Water Across Marlowe","A burst water main left about 4,000 Marlowe households without water on Thursday morning. The utility said crews are working on repairs and expects service to resume by evening. Tankers are stationed at the town hall."),
("R09","Parents Furious as School Bus Route Cut, Board Defends Decision","Dozens of parents packed Tuesday's Tarnwick school board meeting to protest the removal of a bus route. Board chair Dan Weiss said the cut saves $90,000 a year and that a revised route will be considered next month."),
]
for g,t,a in RE: add(g,"emotional_real","REAL","true but urgent/emotional tone",t,a)

RF=[
("R10","Fact-Check: Viral Post Falsely Claims Marlowe Tap Water Is Unsafe","A viral social media post claimed that 95 percent of Marlowe residents fear their tap water. County officials said recent tests met all safety standards, and the post's cited institute does not exist. Fact-checkers rated the claim false."),
("R11","Fact-Check: Rumor That Tarnwick Schools Will Close Is Untrue","Unverified messages circulating on social media claimed all Tarnwick schools would close indefinitely. The district clarified that classes will continue as scheduled and posted the official calendar online."),
("R12","Fact-Check: No Evidence Banks Will Freeze Savings, Treasury Says","A forwarded message claiming banks would freeze savings on Friday is false, the national treasury said in a statement. No such order exists, and the treasury urged the public not to rely on unverified messages."),
]
for g,t,a in RF: add(g,"factcheck_real","REAL","true report debunking a false claim",t,a)

with open("paired_test_set.csv","w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=["id","group","variant","label","tactic","title","article"])
    w.writeheader(); w.writerows(R)
print(len(R),"rows written")
