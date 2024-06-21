<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { Checkbox } from '$lib/components/ui/checkbox';
	import * as Form from '$lib/components/ui/form';
	import { Input } from '$lib/components/ui/input';
	import { formSchema, type FormSchema } from './schema';
	import { type SuperValidated, type Infer, superForm } from 'sveltekit-superforms';
	import { zodClient } from 'sveltekit-superforms/adapters';

	export let data: SuperValidated<Infer<FormSchema>>;

	const form = superForm(data, {
		validators: zodClient(formSchema)
	});

	const { form: formData, enhance } = form;

	let something: boolean = false;
	$: $formData.privacyAck = something;
	$: console.log(something);
</script>

<form method="POST" use:enhance class="flex flex-col">
	<Form.Field {form} name="username">
		<Form.Control let:attrs>
			<Form.Label>Username</Form.Label>
			<Input {...attrs} bind:value={$formData.username} />
		</Form.Control>
		<Form.FieldErrors />
	</Form.Field>

	<Form.Field {form} name="email">
		<Form.Control let:attrs>
			<Form.Label>Email</Form.Label>
			<Input {...attrs} bind:value={$formData.email} />
		</Form.Control>
		<Form.FieldErrors />
	</Form.Field>

	<Form.Field {form} name="password">
		<Form.Control let:attrs>
			<Form.Label>Password</Form.Label>
			<Input {...attrs} bind:value={$formData.password} type="password" />
		</Form.Control>
		<Form.FieldErrors />
	</Form.Field>

	<Form.Field {form} name="privacyAck">
		<Form.Control let:attrs>
			<Form.Label>not password</Form.Label>
			<Checkbox {...attrs} bind:checked={something} />
		</Form.Control>
		<Form.FieldErrors />
	</Form.Field>

	<Button variant="link" href="/login" class="w-fit px-0 text-left">Log in instead</Button>

	<Form.Button>Sign up</Form.Button>
</form>

<style>
	form > :global(*) {
		--destructive: 0 62.8% 60.6%;
	}
</style>
