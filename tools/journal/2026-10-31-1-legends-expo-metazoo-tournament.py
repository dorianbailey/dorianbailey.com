"""Journal: Legends."""
post(dict(
    date="2026-10-31", card_sub="Legends Expo Card Show, Monroeville, PA", card_title="Photographing the MetaZoo $10,000 Tournament",
    slug="legends-expo-metazoo-tournament", section="Event photography",
    title="Photographing the MetaZoo $10,000 Tournament at the Legends Expo",
    seo="Photographing the MetaZoo $10,000 Tournament | Dorian Bailey",
    desc="Event photographer Dorian Bailey on covering the MetaZoo $10,000 cash tournament at the Legends Expo Card Show in Monroeville, Pennsylvania, for MetaZoo TCG.",
    standfirst="Two days of play at the Legends Expo Card Show in Monroeville, Pennsylvania, photographed for MetaZoo TCG.",
    dek="Two days of play in Monroeville, photographed for MetaZoo TCG: the prizes, the players, the broadcast and the last photograph of the weekend.",
    head=jph("legends", 26), card_pos="center 30%",
    about=["Event photography", "MetaZoo", "Trading card game tournaments"],
    body=f"""          <p class="article__lede">In August 2026, MetaZoo TCG commissioned me to photograph its $10,000 cash tournament at the Legends Expo Card Show in Monroeville, Pennsylvania. It was two days of play under convention-hall lights, and the job was to come away with everything the company would need afterward: the prizes, the booth, the players, the broadcast, and one photograph of everyone together at the end.</p>

          <h2>Before the first round</h2>
          <p>The quiet minutes before play starts are when the details get photographed. The first-, second- and third-place prize cards stood on their easels, the MetaZoo booth was set, and an inflatable winged cryptid towered over the hall on its MetaZoo base.</p>
          <p>Those pictures are easy to skip and hard to replace. They&rsquo;re what a brand reaches for when it announces the next event, and once the hall fills up they&rsquo;re much harder to take cleanly.</p>
{jpair((jph("legends", 2), "The first-place prize card"), (jph("legends", 5), "The MetaZoo Trading Card Game booth"))}

          <h2>At the tables</h2>
          <p>A card tournament is a quiet kind of sport. There&rsquo;s no ball to follow, so the story is in hands and faces: a player fanning a hand of cards, another weighing his next move, a reaction across the table when a play lands.</p>
          <p>I worked along the rows through the day, close enough to read the moment and far enough back to stay out of the way. Players are concentrating, and the photographs only work if they forget you&rsquo;re there.</p>
{jpair((jph("legends", 13), "Weighing the next move"), (jph("legends", 17), "A reaction across the table"))}

          <h2>The broadcast</h2>
          <p>Part of the coverage was the production itself: the commentary desk in front of the MetaZoo backdrop, and matches at the feature table played beneath the stream camera. For a brand, those pictures say the event reached people well beyond the hall.</p>
{jpair((jph("legends", 11), "The commentary desk"), (jph("legends", 22), "A match beneath the stream camera"))}

          <h2>The cards themselves</h2>
          <p>It&rsquo;s a trading card game, so the cards get photographs of their own: rows of Old Green Eyes, a Mothman Festival edition card in its sleeve, a Loveland Frogman, and cards being signed at the table.</p>
{jfig(jph("legends", 24), "A Mothman Festival edition card", cls="article__fig--narrow", sizes="(max-width: 820px) 70vw, 400px")}

          <h2>The last photograph</h2>
          <p>When play was done, the whole field gathered beneath the inflatable cryptid for one last photograph. It&rsquo;s the picture that sums up an event, so it&rsquo;s worth getting everyone in place for it before anyone heads for the door.</p>

          <h2>Covering your event</h2>
          <p>Legends was the first of three events I photographed for MetaZoo TCG in three months, followed by the <a href="{J}photography/#mothman">Mothman Festival</a> in Point Pleasant, West Virginia, and the <a href="{J}photography/#green-eyes">Green Eyes Festival</a> in Chickamauga, Georgia. <a href="{J}photography/#legends">The full Legends collection</a> is on the photography page.</p>
          <p>If you&rsquo;re running a tournament, convention, festival or other event, in Erie County or farther afield, I travel for event work.</p>
{cta("Book event photography", "Pick a date and I&rsquo;ll reply to confirm, with rates. Tournaments, conventions, festivals and parties.", [BOOK_PHOTO, RATES])}""",
    particulars=[("Event", "MetaZoo $10,000 cash tournament"), ("Where", "Legends Expo Card Show, Monroeville, Pennsylvania"),
                 ("When", "August 2026"), ("Commissioned by", "MetaZoo TCG"), ("Photographs", "Dorian Bailey"),
                 ("See also", f'<a href="{J}photography/#legends">The Legends collection</a>, <a href="{J}metazoo/">Bailey MetaZoo</a>')],
    images=[jph("legends", n) for n in (26, 2, 5, 13, 17, 11, 22, 24)],
))
