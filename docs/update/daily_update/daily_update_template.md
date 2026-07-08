

The Daily Update Prompt/Template Instruction:  

You need to write a two paragraph update everyday on what we worked on today. It is basically from the experiments we worked on (and why and how) over the past 24 hours, and at the end in end in line what's the plan for tommorrow in plain Engilish.

You can save this update in an md file. You can append the daily with a date in the same md file for a week (7 days, starting from Monday to Sunday). After 7 days, i.e. from the next Monday, you create a new md file to write your daily update. Make sure that the date-range is mentioned in the md filename. 



The style of the udpate will be following:

It's no more than two paragraph update in plain English, and at the end you can write one or two lines about the plan for tomrrow. We can start with: "Today we worked on..." or something along those lines. And before jumping into the nitti-gritty of the update, spend at one sentence that will provide an background/overview, since each update is standalone. 

BUT, at the same time, although each update is standalone, there should be a logical transition or some kind of connection to yesterday's update vs today's update. Always **avoid** negative framing - even if something is not working or missing, that can still be framed in a non-negative way, as an opportunity to work further (i.e. indicating that I am on top of it already). Highlight the milestore and progress of the work (without being explicit or boastful or icky/cringy) - **through explicitly stating what did we actually do in terms of experiments.**    

**IMPORTANT:** The update will be an advisor and wide technical audience facing, and in plain english without jargons or internal references of this project (of files, file names, internal nomeclature, etc.) or metacommentary or imperative / instructional type sentences, and with any abbreviations clarified and if you must use an internal reference that's fully clarified. you need to clarify succicntly the objectives/goals for today, and the progression / milestore so far. You can write things like "2D" instead of "two-dimensional" etc. 

Nowhere should be the internal source or artifacts are mentioned. Optionally, and only if appropriate, you can also briefly mention at the end, what worked and did not work and the pivot made (or plan to make tomorrow). 


IMPORTANT: Make sure there's no redundency in the updates, i.e. repeat same updates, and read the prior updates, if there's any, and **ACTUALLY** inspect what we worked on today (i.e. last 24 hours).

NOTE: Write it in a natural tone/voice, where it shows some personality and not robotic and dry. NEVER use vague words like, "readiness", "story", "staging" etc. 

NOTE: We have been working on this project every single day so far. So there should not be a scenario where there's no new update regarding what we worked on / progress. 




This is an example update from a different work: 

"Today I continued developing the explicit full-antenna 3D BEM model and also worked on a new experimental data-collection plan. All main antenna components, including the Tx/Rx bowties, metallic shield, plastic case, skid, absorber materials, and PCBs, have now been included in the mesh and material-coupling pipeline.

The main challenge I am currently working on is the complex contact around the absorber. One absorber surface is in contact with the metallic shield, while another surface is divided into different regions: part of it touches the shield, part touches the skid, and part is exposed to air. This creates several material–material and material–PEC junctions on the same component, which makes the BEM coupling and interface discretization particularly difficult.

At the moment, this is the most difficult part of the full-antenna model. I am focusing on finding a mathematically reliable way to handle these mixed-contact interfaces, while also checking reciprocity and interface continuity." 