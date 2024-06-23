<script lang="ts">
	import { enhance as exitEnhance } from '$app/forms';
	import type { Selected } from 'bits-ui';
	import * as Select from '$lib/components/ui/select';
	import * as AlertDialog from '$lib/components/ui/alert-dialog';
	import * as Form from '$lib/components/ui/form';
	import { Input } from '$lib/components/ui/input';
	import { formSchema } from './schema';
	import { Button } from '$lib/components/ui/button';
	import type { PageData } from './$types';
	import { superForm } from 'sveltekit-superforms';
	import { Separator } from '$lib/components/ui/separator';
	import { zodClient } from 'sveltekit-superforms/adapters';

	export let data: PageData;

	const models = ['whisper', 'deepgram'] as const;
	type Model = typeof models[number];

	let open = false;
	let modelName: Selected<Model>;

	const form = superForm(data.form, {
		validators: zodClient(formSchema)
	});

	const { form: formData, enhance } = form;
</script>

<svelte:head>
	<title>Your profile</title>
</svelte:head>

<main class="mx-auto max-w-xl py-8">
	<div class="flex flex-row justify-between">
		<div>
			<h1 class="text-5xl">
				Hello, <strong>{data.user.username}</strong>!
			</h1>
			<p class="text-sm text-muted-foreground">
				{data.user.email}
			</p>
			<p class="text-sm text-muted-foreground">
				{data.user.id}
			</p>

			<p>
				You have uploaded {data.fileCount} files and have {data.sessionCount} sessions.
			</p>
		</div>

		<form
			class="float-left mb-0 mr-4 flex flex-col justify-end"
			method="post"
			use:exitEnhance
			action="?/logout"
		>
			<Button class="mb-1" type="submit" variant="destructive">Log out</Button>
		</form>
	</div>

	<Separator class="my-4" />

	<div class="mb-4 flex flex-row justify-between">
		<h1 class="mt-1 text-lg">API keys</h1>
		<Button on:click={() => (open = true)}>Add new key</Button>
	</div>

	{#each data.keyData as key}
		<div class="mb-3 space-y-4">
			<div class="rounded-md bg-gray-800 p-4">
				<div class="flex items-center justify-between">
					<div>
						<h2 class="font-bold text-blue-400">{key.name}</h2>
						<p class="italic text-gray-400">{key.model}</p>
					</div>

					<form method="POST" class="flex flex-col" action="?/deletekey">
						<input hidden value={key.name} id="name" name="name" />
						<Button variant="destructive" type="submit">Delete</Button>
					</form>
				</div>
			</div>
		</div>
	{/each}
</main>

<AlertDialog.Root bind:open>
	<AlertDialog.Content>
		<form method="POST" use:enhance class="flex flex-col" action="?/addkey">
			<Form.Field {form} name="model">
				<Form.Control let:attrs>
					<Form.Label>Model</Form.Label>
					<Select.Root
						selected={modelName}
						onSelectedChange={(v) => {
							v && ($formData.model = v.value);
						}}
					>
						<Select.Trigger class="m-0 w-32">
							{$formData?.model}
						</Select.Trigger>
						<Select.Content>
							{#each models as model}
								<Select.Item value={model}>{model}</Select.Item>
							{/each}
						</Select.Content>
					</Select.Root>

					<input hidden bind:value={$formData.model} name={attrs.name} />
				</Form.Control>
				<Form.FieldErrors />
			</Form.Field>

			<Form.Field {form} name="name">
				<Form.Control let:attrs>
					<Form.Label>Name</Form.Label>
					<Input {...attrs} bind:value={$formData.name} />
				</Form.Control>
				<Form.FieldErrors />
			</Form.Field>

			<Form.Field {form} name="key">
				<Form.Control let:attrs>
					<Form.Label>Key</Form.Label>
					<Input {...attrs} bind:value={$formData.key} />
				</Form.Control>
				<Form.FieldErrors />
			</Form.Field>

			<!-- hack(?) from https://github.com/huntabyte/shadcn-svelte/issues/535, kinda-->
			<Form.Button class="my-2" on:click={() => (open = false)}>Add key</Form.Button>

			<AlertDialog.Cancel on:click={() => (open = false)}>Cancel</AlertDialog.Cancel>
		</form>
	</AlertDialog.Content>
</AlertDialog.Root>
