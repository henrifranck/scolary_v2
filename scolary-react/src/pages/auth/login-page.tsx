import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { useRouter } from '@tanstack/react-router';

import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { cn } from '../../lib/utils';
import { useAuth } from '../../providers/auth-provider';
import { loginWithCredentials } from '../../services/auth-service';

const schema = z.object({
  email: z.string().email('Please enter a valid email'),
  password: z.string().min(6, 'Password must contain at least 6 characters')
});

type FormValues = z.infer<typeof schema>;

export const LoginPage = () => {
  const router = useRouter();
  const {
    store: { login }
  } = useAuth();
  const [formError, setFormError] = useState<string | null>(null);
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting }
  } = useForm<FormValues>({
    defaultValues: { email: '', password: '' }
  });

  const onSubmit = handleSubmit(async (values) => {
    setFormError(null);
    try {
      const response = await loginWithCredentials(values.email, values.password);
      const role = response.is_superuser ? 'admin' : 'student';
      login({
        id: crypto.randomUUID(),
        name: values.email.split('@')[0],
        email: values.email,
        role
      });

      const destination = role === 'admin' ? '/admin/academic-years' : '/';
      router.navigate({ to: destination });
    } catch (error) {
      const message =
        error instanceof Error ? error.message : 'Unable to sign in. Please try again.';
      setFormError(message);
    }
  });

  return (
    <div className="flex min-h-screen items-center justify-center bg-muted/40 p-4">
      <div className="w-full max-w-md space-y-6 rounded-lg border bg-background p-8 shadow-sm">
        <div className="space-y-1 text-center">
          <h1 className="text-2xl font-semibold tracking-tight">Welcome back</h1>
          <p className="text-sm text-muted-foreground">
            Use your existing Scolary credentials to access the dashboard.
          </p>
        </div>
        <form className="space-y-4" onSubmit={onSubmit}>
          <div className="space-y-2">
            <label className="text-sm font-medium" htmlFor="email">
              Email
            </label>
            <Input
              id="email"
              type="email"
              className={cn(errors.email && 'border-destructive text-destructive')}
              placeholder="email@example.com"
              {...register('email')}
            />
            {errors.email ? (
              <p className="text-sm text-destructive">{errors.email.message}</p>
            ) : null}
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium" htmlFor="password">
              Password
            </label>
            <Input
              id="password"
              type="password"
              className={cn(errors.password && 'border-destructive text-destructive')}
              placeholder="••••••••"
              {...register('password')}
            />
            {errors.password ? (
              <p className="text-sm text-destructive">{errors.password.message}</p>
            ) : null}
          </div>
          {formError ? <p className="text-sm text-destructive">{formError}</p> : null}
          <Button className="w-full" disabled={isSubmitting} type="submit">
            {isSubmitting ? 'Signing in…' : 'Sign in'}
          </Button>
        </form>
        <p className="text-center text-xs text-muted-foreground">
          Need an account? Ask your administration staff for an invitation.
        </p>
      </div>
    </div>
  );
};
