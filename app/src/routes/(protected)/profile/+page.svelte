<script lang="ts">
	import { enhance as exitEnhance } from '$app/forms';
	import * as Form from '$lib/components/ui/form';
	import { Input } from '$lib/components/ui/input';
	import { formSchema, type FormSchema } from './schema';
	import { Button } from '$lib/components/ui/button';
	import type { PageData } from './$types';
	import { type SuperValidated, type Infer, superForm } from 'sveltekit-superforms';
	import { zodClient } from 'sveltekit-superforms/adapters';

	export let data: PageData;

	const formsData = data.forms.map(formData => 
		superForm(formData, { resetForm: true }));

	const form = formsData[0];
	const { form: formData, enhance } = form;

	const availableApiNames: string[] = ["deepgram"];
</script>

<svelte:head>
	<title>Your profile</title>
</svelte:head>

<main class="mx-auto max-w-xl py-8">
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

	<div>

			<form method="POST" use:enhance class="flex flex-row">
				<Form.Field {form} name="key">
					<Form.Control let:attrs class="flex flex-row">
						<Form.Label class="pb-0">ApiKey user given name</Form.Label>
						<Input {...attrs} bind:value={$formData.key}/>
					</Form.Control>
					<Form.FieldErrors />
				</Form.Field>

				<div style="pl-10 inline-block">
					<Button style="pb-0">Reset</Button>
					<Form.Button>Update</Form.Button>
				<div>
			</form>
	<div>

	<form class="pt-2" method="post" use:exitEnhance action="?/logout">
		<Button type="submit" variant="destructive">Log out</Button>
	</form>
</main>
