"""Journal: How Take The OddWay plans a road trip."""
post(dict(
    date="2026-11-10", slug="take-the-oddway-road-trip-planner", section="Road trips",
    card_sub="Take The OddWay, a road-trip app",
    card_title="Plan a Road Trip Around the Strange",
    title="How Take The OddWay Plans a Road Trip Around the Strange",
    seo="Road-Trip Planner for Strange Stops | Dorian Bailey",
    desc="How Take The OddWay works as a road-trip planner for the strange: give it a route, filter for cryptids or haunted places, and check each detour before you go.",
    standfirst="Give it a start and a finish and it finds the detours worth taking, from cryptid sites to giant roadside statues, with how far each one pulls you off course.",
    dek="Start with the road, not the destination: how Take The OddWay finds strange stops along a route, and how I&rsquo;d plan a day that&rsquo;s mostly detours.",
    head=jph("green-eyes", 7), card_pos="center 35%",
    about=["Road-trip planner", "Take The OddWay", "Roadside attractions", "Cryptids"],
    body=f"""          <p class="article__lede">Take The OddWay is a road-trip planner for people who would rather see a small cryptid museum than make good time. Give it a route, a start and a finish, and it finds the detours worth taking along the way. Filter by what you want to see, check how far each stop pulls you off course, add the good ones and take the directions with you. I designed and built it, and this is how I&rsquo;d use it to plan a trip that&rsquo;s mostly detours.</p>

          <h2>Start with the road you&rsquo;re already on</h2>
          <p>Most trip planning starts with a destination and works backward. OddWay starts with the drive itself. You&rsquo;re going from Erie to Pittsburgh, or from Cleveland to Cincinnati, and the question it answers is what&rsquo;s strange within reach of that road.</p>
          <p>That changes the trip. A long drive stops being dead time between two places and becomes a string of small decisions: the giant statue, yes; the haunted inn, maybe on the way back; the UFO town, if there&rsquo;s still light.</p>

          <h2>Seven kinds of strange</h2>
          <p>Every place in OddWay&rsquo;s index, nearly 7,000 of them, is filed under one of seven categories, so a trip can be all one thing or a little of everything:</p>
          <ul>
            <li><strong>Cryptids.</strong> Creatures people keep reporting and nobody has caught.</li>
            <li><strong>Folklore.</strong> Local legends, the stories a town tells about itself.</li>
            <li><strong>Haunted.</strong> Hotels, theatres, prisons and back roads with a reputation.</li>
            <li><strong>UFOs.</strong> Sighting sites and the towns that kept the story going.</li>
            <li><strong>Weird history.</strong> True events strange enough to have slipped out of the textbooks.</li>
            <li><strong>Museums.</strong> Small, specific collections.</li>
            <li><strong>Roadside oddities.</strong> Giant objects and odd monuments.</li>
          </ul>
          <p>The filters are the point. A carload that wants haunted hotels and nothing else can have exactly that. A carload that can&rsquo;t agree can leave the filter wide and settle it at each exit.</p>

          <h2>Detour distance decides everything</h2>
          <p>The number that matters on a road trip like this isn&rsquo;t total miles. It&rsquo;s how far each stop pulls you off the route, and OddWay lets you check that before you commit. A roadside oddity two minutes from the interstate is a stretch break. The same thing forty minutes down a county road is the afternoon.</p>
          <p>A few rules I&rsquo;d plan by:</p>
          <ul>
            <li><strong>Set a detour budget for the day</strong>, an hour or two in all, and spend it on purpose. One long detour to something you really want beats five short ones to things you&rsquo;ll forget by dinner.</li>
            <li><strong>Cluster.</strong> Two stops in the same town cost little more than one.</li>
            <li><strong>Daylight first.</strong> Statues, murals and folklore sites are better seen than squinted at. Save the haunted places for evening, if they&rsquo;re open then.</li>
            <li><strong>Check hours with the place itself.</strong> Small museums keep short hours, and some are seasonal. A stop is only worth the detour if the door is open.</li>
            <li><strong>Leave one empty slot.</strong> The best stop on a trip is often the one you spot on a sign.</li>
          </ul>

          <h2>Planning a detour-heavy day</h2>
          <ol class="article__steps">
            <li><strong>Enter the route.</strong> A start and a finish. If the trip runs two days, plan each day as its own route.</li>
            <li><strong>Pick one or two categories.</strong> Start narrow; you can widen the filter if the road is quiet.</li>
            <li><strong>Check the detour on each candidate.</strong> Cut anything that blows the day&rsquo;s budget, unless it&rsquo;s the reason you&rsquo;re going.</li>
            <li><strong>Add the good ones</strong> to the trip, and keep a spare or two in mind.</li>
            <li><strong>Confirm hours and access</strong> with each place before you leave, especially small private museums and anything near private land.</li>
            <li><strong>Take the directions with you</strong> and go stand in front of the thing.</li>
          </ol>

          <h2>Routes worth building</h2>
          <p>A few trips in this journal lend themselves to the method. [[mothman-road-trip-point-pleasant|A Mothman road trip to Point Pleasant, West Virginia]] is a town to plan a whole day around. [[loveland-frogman-ohio|The Loveland Frogman]] is a short detour off a Cincinnati drive. [[lake-erie-monster-bessie|Bessie, the Lake Erie monster]] is a reason to follow the shore west from Erie, and [[bigfoot-in-pennsylvania|Bigfoot in Pennsylvania]] covers the big forests closer to home, and how to look without trespassing.</p>
          <p>The cryptid side of OddWay overlaps with <a href="{J}metazoo/">Bailey MetaZoo</a>, my short videos on the folklore behind the MetaZoo cards. The photograph at the top is from the Green Eyes Festival in Chickamauga, Georgia, which I photographed for MetaZoo TCG in October 2026: Bigfoot and a cloaked, green-eyed figure, both in costume, side by side.</p>

          <h2>Why listings aren&rsquo;t for sale</h2>
          <p>OddWay carries advertising for brands that fit the road, as <a href="{LINKS['oddway_ads']}" rel="noopener">a banner placement or a featured marker on the map</a>. What advertising never buys is a listing. A place is in the index because it&rsquo;s worth the detour, not because it paid, and that&rsquo;s the only way an index like this stays worth trusting.</p>
          <p>I built OddWay end to end: the brand, the research behind every stop and the web app itself, written in Next.js and TypeScript on Supabase. An events listing for cryptid festivals, haunted houses and seasonal mazes is planned but not live yet. More about the project is on <a href="{J}oddway/">the Take The OddWay page</a>, and there&rsquo;s an <a href="{LINKS['shop']}" rel="noopener">OddWay shop</a> too.</p>
{cta("Plan the detour", "Give OddWay a start and a finish, and see what&rsquo;s strange along the way.", [ODDWAY_BTN], status=False)}""",
    particulars=[("App", f'<a href="{LINKS["oddway"]}" rel="noopener">taketheoddway.com</a>'),
                 ("Index", "Nearly 7,000 places in seven categories"),
                 ("Built by", "Dorian Bailey"),
                 ("Advertising", f'<a href="{LINKS["oddway_ads"]}" rel="noopener">For brands that fit the road</a>; listings are never for sale'),
                 ("Photograph", "Costumed cryptids at the Green Eyes Festival, Chickamauga, Georgia, October 2026")],
    images=[jph("green-eyes", 7)],
))
