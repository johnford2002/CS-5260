# Schedule Evaluation

## Undiscounted Reward of a Schedule

The reward of a schedule can be positive or negative, and is the difference between the state quality of the end state of the schedule for a country and the state quality of the start state for the same country.
  
A schedule can benefit or degrade countries to varying extents, so each country that participates in a schedule probably has a different reward for a given schedule.
  
Remember, you design how to implement state quality for a country as discussed above, but you must use the difference between the beginning and end state qualities as the undiscounted reward.

**For Country C<sub>i</sub> and Schedule S<sub>j</sub>:**  
<code>
R(C<sub>i</sub>, S<sub>j</sub>) = Q<sub>end</sub>(C<sub>i</sub>, S<sub>j</sub>) – Q<sub>start</sub>(C<sub>i</sub>, S<sub>j</sub>) 
</code>


## Discounted Reward of a Schedule

The Discounted Reward comes from the end state of a schedule, but the farther the end state is into the future, the less it counts for a country. If there are `N` time steps in a schedule, then the discounted expected reward for a country is:  
<code>
DR(C<sub>i</sub>, S<sub>j</sub>) = &gamma;N ∗ (Q<sub>end</sub>(C<sub>i</sub>, S<sub>j</sub>) – Q<sub>start</sub>(C<sub>i</sub>, S<sub>j</sub>)), where 0 <= &gamma; < 1
</code>



For many sequential decision problems (Chapter 17, Russell and Norvig; Chapter 9, Poole and Mackworth), each state in the sequence comes with some reward (positive or negative/penalty), and the utility of the sequence is the sum of discounted state rewards, but in Part 1, we assume that the entire reward comes at the end state only. Nonetheless, your system can (and probably will) compute the discounted end state quality for every partial schedule on the search frontier, which could be used to organize the frontier as a priority queue (refer to the Expected Utility of a Schedule section). You will experiment with different values of gamma and can report results on the Discussion Forum.

## Probability that a Schedule will Succeed

Even when there is no uncertainty associated with an operator’s effects when the operator is applied, and therefore no uncertainty associated with a legal schedule’s effects when the schedule is applied, there remain other sources of uncertainty in the schedule. Notably, other countries referenced in the schedule may not “go along” with the schedule if an attempt were made to “execute” it in the real world. You will use state qualities for other countries as well as your own country, to judge the likelihood that a schedule will be accepted by all parties. Notably, if a schedule references a number of other countries, then the more that the schedule benefits each of the referenced countries (i.e., in terms of discounted reward), the chances that they will agree to the schedule increase. 
  
The probability that a country, <code>C<sub>i</sub></code>, will participate in a schedule, <code>S<sub>j</sub></code>, is computed by the [logistic function](https://en.wikipedia.org/wiki/Logistic_function).

<code>
&#x192;(x) = L &#47; ( 1 + e<sup>-k(x-x<sub>0</sub>)</sup> )
</code>  
  

The variable `x` corresponds to <code>DR(C<sub>i</sub>, S<sub>j</sub>)</code> and `L = 1`, and you can experiment with different values of <code>x<sub>0</sub></code> and `k` (but use <code>x<sub>0</sub> = 1</code> and `k = 1` as starting points). Think about, and report on, how different parameter settings might reflect biases in the real world (e.g., a reason for shifting <code>x<sub>0</sub></code> might be to reflect opportunity costs — what other benefits might await a patient country?).
  
Given the individual probabilities of each referenced country participating, <code>P(C<sub>i</sub>, S<sub>j</sub>)</code>, the probability that a schedule will be accepted and succeed, <code>P(S<sub>j</sub>)</code>, could be computed in a number of ways (e.g., the min of the probabilities, reflecting the weakest link), but we’ll use the product of the probabilities of the individual <code>P(C<sub>i</sub>, S<sub>j</sub>)</code>.
  
Note that the strategy for estimating the probability that a schedule is accepted (i.e., will be accepted by all parties to the schedule) and succeeds, does not come from statistics accumulated over data from the “real world” (to include game play) as we might think is ideal, but our method draws from an information theoretic tradition of estimating probabilities of “events” from the “descriptions” of those events. An assumption in this description-driven methodology is a bias that more “complicated” descriptions represent lower probability events. It is a quantification of Occam’s razor.
  
This is the one way (probably the only way given the time constraints in Part 1) that your scheduler for your country will take into account the state qualities of other countries, as well as your own. It has the effect of countering ill-considered greed.   

## Expected Utility of a Schedule

The probability that a schedule will be accepted and succeed (which takes into account other countries) multiplied by the discounted reward for your country (self) is the central factor in computing the expected utility of a schedule (<code>S<sub>j</sub></code>) for your country (self, ci). But what is the cost to a country of producing a schedule that would ultimately fail? For simplicity, let the cost of the failure case be a negative constant, `C`. You choose `C`, with justification given, or if you are more ambitious, design a more general function to represent the failure cost: 

<code>
EU(C<sub>i</sub>, S<sub>j</sub>) = (P(S<sub>j</sub>) ∗ DR(C<sub>i</sub>, S<sub>j</sub>)) + ((1 − P(S<sub>j</sub>)) ∗ C), where C<sub>i</sub> = self
</code>
