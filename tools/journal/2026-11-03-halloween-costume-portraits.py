"""Journal: Halloween costume portraits."""
post(dict(
    date="2026-11-03", slug="halloween-costume-portraits", section="Portraits",
    card_sub="Two couples, twenty minutes of golden hour",
    title="Halloween Costume Portraits at Golden Hour",
    seo="Halloween Costume Portraits at Golden Hour | Dorian Bailey",
    desc="Halloween costume portraits at golden hour: Freddy Krueger and Nancy, Clark Kent and Supergirl, and how to plan costume photos for couples, by Dorian Bailey.",
    standfirst="Two couples, two famous pairings and about twenty minutes of late-October light: the portraits from Halloween 2026, and how I&rsquo;d plan a session like it.",
    dek="Freddy and Nancy, Clark Kent and Supergirl, and twenty minutes of golden hour: what made the Halloween portraits, and how to plan your own.",
    head=jph("halloween", 2), card_pos="center 30%",
    about=["Halloween costume portraits", "Couples photography", "Golden hour portraits"],
    body=f"""          <p class="article__lede">On Halloween 2026 I photographed two couples in costume: one as Freddy Krueger and Nancy from <em>A Nightmare on Elm Street</em>, the other as Clark Kent and Supergirl, and then all four together. These Halloween costume portraits were made between about 5:40 and 6:00 p.m., golden hour on the last day of October, among autumn trees and on a decorated porch. Costume portraits work when the costume gives people something to do and the light does the rest. Here is what made these frames, and how I&rsquo;d plan a session like it.</p>

          <h2>Why golden hour suits costume portraits</h2>
          <p>Golden hour is the stretch before sunset when the sun sits low and its light turns warm and soft. On October 31, 2026, Erie&rsquo;s sunset came at 6:15 p.m., which puts the best of the late-October light at about the time these frames were made.</p>
          <p>Low light matters more for costumes than for most portraits. A hat brim, like Freddy&rsquo;s fedora, throws a hard shadow across the eyes when the sun is high; late in the day the light reaches in under the brim. Warm light is kind to skin, makeup and fabric alike, and it turns October leaves into a Halloween backdrop on its own. The porch, with its skeleton and its decorations, was a bonus.</p>

          <h2>Freddy and Nancy: play the scene</h2>
          <p>Freddy Krueger&rsquo;s look goes back to Wes Craven&rsquo;s 1984 film: a red-and-green striped sweater, a brown fedora and a bladed glove. The glove is the whole character in one prop, and nearly every frame of this couple is built around it: tilting Nancy&rsquo;s chin, resting on her shoulder, lying across her sweater, curling over her shoulder as she gasps on the porch.</p>
          <p>Nancy&rsquo;s part is to play it almost straight. Her mock gasp works because it&rsquo;s plainly a performance, and the calmer frames work because she looks entirely unbothered while the claws hover. Her pink sweater helps too. It sits against his stripes and the orange trees, and nothing clashes because nothing is trying to match.</p>
{jpair((jph("halloween", 1), "Freddy Krueger tilting up Nancy&rsquo;s chin"), (jph("halloween", 5), "His glove across her sweater"))}

          <h2>Clark Kent and Supergirl: the reveal</h2>
          <p>The second couple called for the opposite mood: open, cheerful and a little corny on purpose. The superhero pose everyone knows is Clark Kent pulling open his shirt to show the S underneath, and it&rsquo;s the centerpiece of this set, with Supergirl&rsquo;s fist raised in the air beside him.</p>
          <p>The rest of their set is lighter still: the two of them smiling at each other under the leaves, and Superman carrying Supergirl, both of them grinning. Their costumes share a palette of red, blue and yellow without being the same outfit, which is the whole trick of dressing as a pair.</p>
{jpair((jph("halloween", 8), "Clark Kent pulls open his shirt to show the S"), (jph("halloween", 9), "Superman carrying Supergirl"))}
          <p>The lesson carries over to any couple. A costume with a famous gesture hands you a pose, and a pose with a little action in it gets real smiles faster than being told to look at each other.</p>

          <h2>All four together</h2>
          <p>The group frame is the one that sums up the evening, so it&rsquo;s worth getting before anyone&rsquo;s makeup slips or a prop goes missing. Two couples in two very different moods could easily look like two photographs stitched together. A single row under the same trees, with the same warm light on every face, makes it one picture: horror on the left, comic book on the right.</p>
{jfig(jph("halloween", 11), "Freddy, Nancy, Supergirl and Clark Kent together beneath the autumn trees")}

          <h2>Planning your own costume portraits</h2>
          <ul>
            <li><strong>Book the hour before sunset.</strong> Look up the sunset time for your date (<a href="https://sunrise-sunset.org/us/erie-pa" rel="noopener">here it is for Erie</a>) and start about an hour ahead of it.</li>
            <li><strong>Mind the clock change.</strong> In 2026 the clocks fell back the morning after Halloween, and Erie&rsquo;s sunset moved from 6:15 p.m. to 5:13 p.m. overnight. A session in early November starts an hour earlier by the clock than one in late October.</li>
            <li><strong>Choose costumes with a prop or a gesture.</strong> A glove, a pair of glasses, a shirt to pull open: anything that gives hands something to do.</li>
            <li><strong>Pick one mood per couple.</strong> Menace or comedy, sweet or silly. Committing to one makes every frame easier to direct and easier to read.</li>
            <li><strong>Keep to two settings.</strong> Autumn trees and a decorated porch were plenty for twenty minutes. Every move to a new spot spends light.</li>
            <li><strong>Check masks and makeup in daylight</strong>, before the light starts to go, and bring whatever you need for quick repairs.</li>
            <li><strong>Plan for the cold.</strong> A coat to throw on between setups keeps everyone comfortable, and comfortable people smile.</li>
          </ul>

          <h2>Booking a portrait session</h2>
          <p>I photograph portraits, couples and families on location around Erie County. If you&rsquo;re planning a couple&rsquo;s session in any season, [[couples-photos-erie-county|my guide to couples and engagement photos in Erie County]] covers places, timing and what to wear, and [[senior-pictures-erie-county|the guide to senior picture locations]] has more spots with good light. The rest of the evening is in <a href="{J}photography/#halloween">the Halloween collection</a>, and every kind of session I offer is listed on <a href="{J}photography/#types">the photography page</a>.</p>
{cta("Book a portrait session", "Pick a date and I&rsquo;ll reply to confirm, with rates. Portraits, couples and families, on location around Erie County.", [BOOK_PHOTO, RATES])}""",
    particulars=[("When", "October 31, 2026, about 5:40 to 6:00 p.m."),
                 ("Costumes", "Freddy Krueger and Nancy; Clark Kent and Supergirl"),
                 ("Settings", "Autumn trees and a decorated porch"),
                 ("Photographs", "Dorian Bailey"),
                 ("See also", f'<a href="{J}photography/#halloween">The Halloween collection</a>')],
    images=[jph("halloween", n) for n in (2, 1, 5, 8, 9, 11)],
))
