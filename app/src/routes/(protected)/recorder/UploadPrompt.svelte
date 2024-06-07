<script lang="ts">
	import { Input } from '$lib/components/ui/input';
	import { parsePromptFile, readAsPlaintext, type Prompt } from './recorder';

	export let onPromptUpload: (prompt: { filename: string; prompts: Prompt[] }) => void = () => {};

	let error: { message: string } | null = null;

	async function handlePromptUpload(event: Event) {
		if (!(event.target instanceof HTMLInputElement)) {
			throw new Error('Event target is not an input element');
		}

		const { target: input } = event;

		if (input.files === null || input.files.length != 1) {
			error = { message: "Didn't receive one file" };
			return;
		}

		const file = input.files[0];

		if (file.type !== 'text/plain') {
			error = { message: 'File was not plain text' };
			return;
		}

		const prompts = parsePromptFile(await readAsPlaintext(file));

		onPromptUpload({ filename: file.name, prompts });
	}
</script>

<div class="mx-auto grid h-full w-fit content-center text-center">
	<div class="mx-auto w-fit pb-4 text-xl">Please upload a prompt to record</div>

	<Input type="file" accept=".txt" onchange={handlePromptUpload} />
</div>
{#if error !== null}
	{error.message}
	<!-- TODO: Show error -->
{/if}
