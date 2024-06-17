<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { sessionTable } from '$lib/database/schema';
	import { humanSensibleDate } from '$lib/time';
	import * as Tooltip from '$lib/components/ui/tooltip';

	import * as ContextMenu from '$lib/components/ui/context-menu';
	import * as AlertDialog from '$lib/components/ui/alert-dialog';

	export let session: typeof sessionTable.$inferSelect;

	export let onDeleteSession: (fileId: string) => void = () => {};

	let deleteAlertOpen = false;

	async function deleteSession() {
		await fetch('?/deleteSession', {
			method: 'POST',
			body: JSON.stringify(session.id)
		}).then(async (response) => {
			if ((await response.json()).status == 204) {
				console.log('success?');
				onDeleteSession(session.id);
			}
		});
	}

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
		<ContextMenu.Root>
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
			<ContextMenu.Content>
				<ContextMenu.Item on:click={() => exportSession()}>Export</ContextMenu.Item>
				<ContextMenu.Item on:click={() => (deleteAlertOpen = true)}>Delete</ContextMenu.Item>
			</ContextMenu.Content>
		</ContextMenu.Root>
	</Tooltip.Trigger>

	<Tooltip.Content>
		<p>{session.name}</p>
	</Tooltip.Content>
</Tooltip.Root>

<AlertDialog.Root bind:open={deleteAlertOpen}>
	<AlertDialog.Content>
		<AlertDialog.Header>
			<AlertDialog.Title>Are you absolutely sure?</AlertDialog.Title>
			<AlertDialog.Description>
				This action cannot be undone. This will permanently delete your session and remove your data
				from our servers.
			</AlertDialog.Description>
		</AlertDialog.Header>
		<AlertDialog.Footer>
			<AlertDialog.Cancel>Cancel</AlertDialog.Cancel>
			<AlertDialog.Action on:click={() => deleteSession()}>Continue</AlertDialog.Action>
		</AlertDialog.Footer>
	</AlertDialog.Content>
</AlertDialog.Root>
