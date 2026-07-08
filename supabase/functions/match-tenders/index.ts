// supabase/functions/match-tenders/index.ts
// Deno Edge Function – cron-triggered tender matcher
import "jsr:@supabase/functions-js/edge-runtime.d.ts"
import { createClient } from "https://esm.sh/@supabase/supabase-js@2"

Deno.serve(async (_req) => {
  const supabase = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
  )
  const { data: tenders } = await supabase.from("tenders").select("tender_id").limit(1)
  return new Response(JSON.stringify({ ok: true, count: tenders?.length ?? 0 }),
    { headers: { "Content-Type": "application/json" }})
})
