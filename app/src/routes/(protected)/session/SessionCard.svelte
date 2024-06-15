<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { sessionTable } from '$lib/database/schema';
	import { humanSensibleDate } from '$lib/time';
	import * as Tooltip from '$lib/components/ui/tooltip';

	import * as ContextMenu from '$lib/components/ui/context-menu';

	export let session: typeof sessionTable.$inferSelect;

	async function exportSession() {
		let response = await fetch('?/exportSession', {
			method: 'POST',
			body: JSON.stringify(session.id)
		});
		let dataString = await response.json();
		if (dataString.status === 200) {
			let data = await JSON.parse(dataString['data']);
			let name = (await JSON.parse(data)).name;
			let blob = new Blob([data], { type: 'application/json' });

			// Download the json file
			let link = document.createElement('a');

			link.href = URL.createObjectURL(blob);

			link.download = `${name}-spectral.json`;

			document.body.appendChild(link);

			link.click();

			document.body.removeChild(link);
			return;
		}
		// in case the session could not be found for
		console.error('session could not be exported');
	}
</script>

<Tooltip.Root>
	<Tooltip.Trigger>
		<ContextMenu.Trigger>
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

					<div class="text-sm">
						Modified: {humanSensibleDate(session.modifiedTime)}
					</div>
				</section>
			</Button>
		</ContextMenu.Trigger>
	</Tooltip.Trigger>

	<Tooltip.Content>
		<p>{session.name}</p>
	</Tooltip.Content>

	<ContextMenu.Content>
		<ContextMenu.Item on:click={() => exportSession()}>Export</ContextMenu.Item>
	</ContextMenu.Content>
</Tooltip.Root>
