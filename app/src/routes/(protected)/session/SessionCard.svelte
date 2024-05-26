<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { sessionTable } from '$lib/database/schema';
	import { humanSensibleDate } from '$lib/time';
	import * as Tooltip from '$lib/components/ui/tooltip';

	export let session: typeof sessionTable.$inferSelect;

	const msInHour = 1000 * 60 * 60;
	$: msModifiedCreation = session.modifiedTime.getTime() - session.creationTime.getTime();
</script>

<Tooltip.Root>
	<Tooltip.Trigger>
		<Button class="h-fit px-6 py-8" variant="outline" href="session/{session.id}">
			<section class="flex flex-col items-start">
				<h2 class="w-[12rem] overflow-hidden text-ellipsis text-left text-xl">
					{session.name}
				</h2>

				<span class="mb-3 text-xs text-muted-foreground">
					{session.id}
				</span>

				<div class="text-sm">
					Created: {humanSensibleDate(session.creationTime)}
				</div>

				<div class="text-sm" class:opacity-0={msModifiedCreation > msInHour}>
					Modified: {humanSensibleDate(session.creationTime)}
				</div>
			</section>
		</Button>
	</Tooltip.Trigger>

	<Tooltip.Content>
		<p>{session.name}</p>
	</Tooltip.Content>
</Tooltip.Root>
