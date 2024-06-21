<script lang="ts">
	import { parsePromptFile, readAsPlaintext, type Prompt } from './recorder';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { Button } from '$lib/components/ui/button';
	import { Textarea } from '$lib/components/ui/textarea';
	import InfoIcon from 'lucide-svelte/icons/info';
	import * as Dialog from '$lib/components/ui/dialog';

	let participantId: string = '';
	let participantNote: string = '';
	let fileName: string | null = null;
	let prompts: Prompt[] | null = null;

	let promptErrorText = '';

	export let onFormSubmit: (
		participantId: string,
		participantNote: string,
		prompt: { fileName: string; prompts: Prompt[] }
	) => void = () => {};

	function formSubmit() {
		if (fileName && prompts) {
			onFormSubmit(participantId, participantNote, { fileName: fileName, prompts: prompts });
		} else {
			promptErrorText = 'Upload a prompts .txt file!';
		}
	}

	async function handlePromptUpload(event: Event) {
		if (!(event.target instanceof HTMLInputElement)) {
			throw new Error('Event target is not an input element');
		}

		fileName = null;
		prompts = null;

		const { target: input } = event;

		if (input.files === null || input.files.length != 1) {
			promptErrorText = 'No file was uploaded';
			return;
		}

		const file = input.files[0];

		if (file.type !== 'text/plain') {
			promptErrorText = 'The file was not a correct .txt file';
			return;
		}

		fileName = file.name;
		prompts = parsePromptFile(await readAsPlaintext(file));
		promptErrorText = '';
	}

	function getSampleSession() {
		let url = '/samples/prompts/text-7.txt';
		const a = document.createElement('a');
		a.href = url;
		a.download = 'sample-prompts.txt';
		document.body.appendChild(a);
		a.click();
		document.body.removeChild(a);
	}
</script>

<!-- <div class="mx-auto grid h-full w-fit content-center text-center">
	<div class="mx-auto w-fit pb-4 text-xl">Please upload a prompt to record</div>

	<Input type="file" accept=".txt" onchange={handlePromptUpload} />
</div> -->
<div class="flex h-full w-full items-center justify-center">
	<form on:submit={() => formSubmit()} class="flex h-3/4 w-1/3 flex-col">
		<h2 class="mb-2 text-2xl font-bold">Prompt Recorder information</h2>
		<div class="mb-4">
			<Label>Participant id</Label>
			<Input bind:value={participantId} />
		</div>
		<div class="mb-4">
			<Label>Notes about participant</Label>
			<Textarea bind:value={participantNote} />
		</div>

		<div class="mb-4">
			<div class="flex">
				<Label>File with prompts</Label>
				<Dialog.Root>
					<Dialog.Trigger><InfoIcon class="ml-0.5 h-4 w-4 pb-1"></InfoIcon></Dialog.Trigger>
					<Dialog.Content class="sm:max-w-[425px]">
						<Dialog.Header>
							<Dialog.Title>Information about prompt file format</Dialog.Title>
							<Dialog.Description>
								The prompt file should be a txt file and the prompts should written in the following
								format:
							</Dialog.Description>
						</Dialog.Header>
						&lt;id&gt; &lt;prompt&gt; <br />
						&lt;id&gt; &lt;prompt&gt; <br />
						...
						<Dialog.Footer>
							<Button onclick={getSampleSession}>Click here to get a sample file</Button>
						</Dialog.Footer>
					</Dialog.Content>
				</Dialog.Root>
				<Label class="text-red-600">
					{promptErrorText}
				</Label>
			</div>
			<Input type="file" accept=".txt" onchange={handlePromptUpload} />
		</div>

		<Button on:click={formSubmit}>Start recording session</Button>
	</form>
</div>

<!-- <AlertDialog.Root bind:open={infoOpen}>
	<AlertDialog.Content>
		<AlertDialog.Header>
			<AlertDialog.Title>The upload prompts must have the following format:</AlertDialog.Title>
			<AlertDialog.Description>
				&lt;id&gt; &lt;prompt&gt; <br>
				&lt;id&gt; &lt;prompt&gt; <br>
				...
			</AlertDialog.Description>
		</AlertDialog.Header>
		<AlertDialog.Footer>
			<AlertDialog.Cancel>Close menu</AlertDialog.Cancel>
			<AlertDialog.Action on:click={getSampleSession}>Download sample prompts</AlertDialog.Action>
		</AlertDialog.Footer>
	</AlertDialog.Content>
</AlertDialog.Root> -->
