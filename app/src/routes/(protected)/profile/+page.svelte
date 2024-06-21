<script lang="ts">
	import { enhance as exitEnhance } from '$app/forms';
	import * as Select from '$lib/components/ui/select';
	import * as AlertDialog from '$lib/components/ui/alert-dialog';
	import * as Form from '$lib/components/ui/form';
	import { Input } from '$lib/components/ui/input';
	import { formSchema, type FormSchema } from './schema';
	import { Button } from '$lib/components/ui/button';
	import type { PageData } from './$types';
	import { type SuperValidated, type Infer, superForm } from 'sveltekit-superforms';
	import { Separator } from '$lib/components/ui/separator';
	import { zodClient } from 'sveltekit-superforms/adapters';

	export let data: PageData;

	const formsData = data.forms.map(formData => 
		superForm(formData, { resetForm: true }));

	const form = formsData[0];
	const { form: formData, enhance } = form;

	const availableApiNames: string[] = ["deepgram"];

	let open = false;
	let modelName;
	let models = ["whisper", "deepgram"]; 
	let newApiKey;
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


		<form class="float-left mr-4 mb-0 flex flex-col justify-end" method="post" use:exitEnhance action="?/logout">
			<Button class="mb-1" type="submit" variant="destructive">Log out</Button>
		</form>
	</div>

	<Separator class="my-4"/>

	<div class="flex flex-row justify-between mb-4">
		<h1 class="text-lg mt-1">API keys</h1>
		<Button on:click={() => (open = true)}>Add new key</Button>
	</div>

	{#each apiKeys as key}
  <div class="space-y-4">
      <div class="bg-gray-800 p-4 rounded-md">
          <div class="flex justify-between items-center">
              <div>
                  <h2 class="text-blue-400 font-bold">{key.name}</h2>
                  <p class="text-gray-400 italic">{key.model}</p>
              </div>
              <Button variant="destructive" on:click={() => {deleteKey(key);}}">Delete</Button>
          </div>
      </div>
    </div>
</main>

<AlertDialog.Root bind:open>
	<AlertDialog.Content>
		<AlertDialog.Header>
			<AlertDialog.Title>Select the model</AlertDialog.Title>
			<AlertDialog.Description>
				<Select.Root bind:selected={modelName}>
					<Select.Trigger class="m-0 w-32">
						{modelName?.value}
					</Select.Trigger>
					<Select.Content>
						{#each models as model}
							<Select.Item value={model}>{model}</Select.Item>
						{/each}
					</Select.Content>
				</Select.Root>
			</AlertDialog.Description>
			<AlertDialog.Title>Enter the key</AlertDialog.Title>
			<AlertDialog.Description>
				<Input type="text" name="apiKeyField" bind:value={newApiKey}></Input>
			</AlertDialog.Description>
		</AlertDialog.Header>
		<AlertDialog.Footer>
			<AlertDialog.Cancel on:click={() => (open = false)}>Cancel</AlertDialog.Cancel>
			<AlertDialog.Action on:click={() => {addKey(modelName, newApiKey);}}>Add key</AlertDialog.Action>
		</AlertDialog.Footer>
	</AlertDialog.Content>
</AlertDialog.Root>

