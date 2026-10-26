# Interviewing rules

Sourced rules for getting what an individual is out of its author's head when the notes are thin. The interviewer drafts every answer from the notes; the author accepts or corrects it.

## Turn

- One turn asks every open conflict, the next every open question, each with a draft answer from the notes, then "correct, or what is wrong?" (teachback, Pask 1976)
- Only root questions are asked: draft every open question from the notes and the accepted answers, find the few unknowns the drafts hinge on, and ask those; a question its roots settle is filled from them and shown only when a root answer breaks its draft
- A draft is a list of claims, one line each, numbered across the turn and tagged today, next or later
- The author corrects only the wrong claims; a claim left uncorrected is accepted
- A correction shows only the claims that changed, as a diff, `-` the old line and `+` the new; the unchanged claims stay out
- No prose around it beyond the lines the workspace instructions require: the questions, the drafts, the ask; a conflict adds one line of linked sources under its question
- An unsure acceptance gets one confidence probe (Willis 1999)
- On resume, the open conflicts come first, then the questions still asked; an asked row without a draft gets one when asked again
- A fix an answer calls for in another note goes to the fixes section of the ledger, never into a turn

## Ledger

- A note beside the individual's note, `type` ResearchReport, `noteRole: scratch`, `subject` the individual, named "Working Note What <Name> Is"; when one exists, continue it; read it from disk at every turn, never from a snapshot
- A goal checklist of four competency questions: what kind of thing (A2), what for (B1), for whom (B3), unlike what (C4) (Grüninger and Fox 1995); a goal is checked when its question is accepted
- A questions section, one numbered item per question: its id, status and question; under it the draft claims, the author's words and the accepted answer; the draft enters when the question is asked, the answer only when accepted
- Status is open (not yet asked), asked (awaiting an answer), accepted, settled (filled from a root answer) or superseded; nothing is overwritten, a superseded answer names its replacement (Nygard 2011)
- A conflicts section, one numbered item per clash: its id X1, X2 and on, stasis, status and the point in dispute; under it one line per source with its link and claim, the repository verdict for a fact clash, and the draft
- A fixes section, one item per edit the answers call for in another note: its link, the property or section, and the proposed text

## Order

Facts first, then purpose, then contrast, then genus (Posterior Analytics II.1). Core questions:

| #  | Question                                                     | Source                                         |
| -- | ------------------------------------------------------------ | ---------------------------------------------- |
| D1 | What happens in a typical session with it?                   | grand tour question, Spradley 1979             |
| D4 | The notes claim A. True?                                      | an sit before quid sit, Quintilian III.6.80    |
| D5 | The repository against your picture: what is missing on either side? | reflexion model, van Deursen et al. 2004 |
| B1 | What is it for? What is lost without it?                     | final cause, Physics II.3; Debian DevRef 6.2   |
| B2 | When do you reach for it, and to get what?                   | job story, Klement 2013                        |
| B3 | Who uses it, and which systems does it talk to?              | system context, C4; arc42 section 3            |
| C1 | Its neighbours: alternatives, predecessors, your projects?   | elements, Kelly repertory grid                 |
| C2 | Of three neighbours, which two are alike, and why?           | triad elicitation, Kelly 1955                  |
| C4 | How does it differ from its nearest neighbour?               | contrast question, Spradley 1979               |
| A2 | What kind of thing is it, nearest kind?                      | genus, Topics I.5; ISO 704 6.3.5               |
| A3 | Its siblings in that kind, and the difference to each?       | delimiting characteristics, ISO 704            |
| A6 | Does the draft line cover every case, exclude every sibling? | Topics VI.1                                    |
| A7 | Can the line replace the name without changing the meaning?  | substitution, ISO 704 6.3.4                    |

D4 is a template: at ground time it becomes one row per claim the notes make on what the individual is, D4a, D4b and on, each naming the claim and its source; a claim already in a conflict gets no row.

Held back for an answer that stays open: D2 one real case (Critical Decision Method, Klein et al. 1989), D3 what came before (switch interview, Moesta and Spiek), C5 why a difference matters (laddering, Hinkle 1965), A4 essential or only true now (predicables, Topics I.8).

## Conflicts

- Clashes among the notes go to the conflicts section at ground time and are asked first
- Check every new answer against the accepted ones; no new question while a conflict stands
- Triage by stasis: fact, definition or quality (Quintilian III.6); fact clashes are asked first, then definition, then quality; a clash takes the question statuses
- The interviewer settles a fact conflict against the repository; the verdict, convergence, divergence or absence, goes into the conflict item with the command run and its result, and becomes its draft, which the author still accepts or corrects
- A definition conflict revises the less credible side, the draft or the accepted answer (reflective equilibrium, Daniels, SEP); credibility ranks code and notes over recollection, explicit over inferred, recent over old
- Before forcing a fix, ask whether both hold at different times or the view changed (Rubin and Rubin 2012, ch. 8)

## Stop

The interview ends when the four goal questions are accepted. The fixes section is shown for one yes or no, and each fix applied runs `just validate` on its note. The accepted answers are appended verbatim to the grounding file, and step 2 of the skill goes on to the map.

## Sources

- Spradley, The Ethnographic Interview, 1979
- Pask, Conversation Theory, 1976
- Willis, Cognitive Interviewing, 1999
- Grüninger and Fox, Methodology for the Design and Evaluation of Ontologies, 1995
- Nygard, Documenting Architecture Decisions, 2011: https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- Klement, Replacing the User Story with the Job Story, 2013
- C4 model, system context: https://c4model.com/diagrams/system-context
- arc42, context and scope: https://docs.arc42.org/section-3/
- Kelly Society, repertory grids: https://kellysociety.org/repgrids.html
- van Deursen et al., Symphony, CWI SEN-R0404, 2004
- Klein, Calderwood and MacGregor, Critical Decision Method, 1989
- ISO 704:2009, as quoted in: https://arxiv.org/pdf/1609.05170
- Aristotle, Topics, Physics II, Posterior Analytics II; Quintilian, Institutio Oratoria III.6
- Daniels, Reflective Equilibrium, SEP: https://plato.stanford.edu/entries/reflective-equilibrium/
- Rubin and Rubin, Qualitative Interviewing, 2012
