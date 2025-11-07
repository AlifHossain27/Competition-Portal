"use client";

import { z } from "zod";
import { useForm } from "react-hook-form";
import { useRouter } from "next/navigation";
import React, { useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormMessage,
} from "@/components/ui/form";
import { toast } from "sonner";
import { Lock, Mail, Eye, EyeOff } from "lucide-react";
import { logIn, logOut } from "@/redux/features/auth-slice";
import { useDispatch } from "react-redux";
import { AppDispatch } from "@/redux/store";
import Link from "next/link";

import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from "@/components/ui/signInCard";

const formSchema = z.object({
  email: z.string().email({ message: "Please enter a valid email address." }),
  password: z
    .string()
    .min(8, { message: "Password must be at least 8 characters." }),
});

export default function LoginPage() {
  const router = useRouter();
  const dispatch = useDispatch<AppDispatch>();
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;
  const [showPassword, setShowPassword] = useState(false);

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: { email: "", password: "" },
    mode: "onChange",
  });

  const {
    control,
    handleSubmit,
    formState: { errors },
  } = form;

  async function onSubmit(values: z.infer<typeof formSchema>) {
    const formData = new URLSearchParams();
    formData.append("username", values.email);
    formData.append("password", values.password);

    try {
      const resp = await fetch(`${API_BASE_URL}/api/auth/token/`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData,
        credentials: "include",
      });

      if (resp.ok) {
        dispatch(logIn());
        toast("Login Successful");
        router.push("/");
      } else {
        dispatch(logOut());
        toast.error(`Login Failed (Status ${resp.status})`);
      }
    } catch (err) {
      toast.error("Network error, please try again.");
    }
  }

  return (
    <main className="min-h-screen flex items-center justify-center bg-gradient-to-b from-primary/12 to-background">
      <div className="w-full max-w-md">
        {/* Card Wrapper */}
        <Card className="border-border bg-card bg-gradient-to-b from-primary/10 to-background shadow-xl">
          {/* Header */}
          <CardHeader>
            <div className="bg-white/60 p-3 rounded-full mb-3 shadow-sm">
              <Lock className="w-6 h-6 text-gray-700" />
            </div>
            <CardTitle className="text-xl font-semibold text-foreground">
              Sign in with email
            </CardTitle>
            <CardDescription className="text-center">
              Access your university clubs and events easily.
            </CardDescription>
          </CardHeader>

          {/* Content */}
          <CardContent>
            <Form {...form}>
              <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
                {/* EMAIL FIELD */}
                <FormField
                  control={control}
                  name="email"
                  render={({ field }) => (
                    <FormItem>
                      <div className="relative h-12">
                        <Mail
                          className={`absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 transition-colors duration-200
                          ${
                            !errors.email && field.value
                              ? "text-foreground"
                              : "text-gray-400"
                          }`}
                        />
                        <FormControl>
                          <Input
                            type="email"
                            autoComplete="off"
                            {...field}
                            placeholder="Email"
                            className="pl-10 pr-3 h-12 text-[15px] focus:ring-2 focus:ring-gray-300"
                          />
                        </FormControl>
                      </div>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                {/* PASSWORD FIELD */}
                <FormField
                  control={control}
                  name="password"
                  render={({ field }) => (
                    <FormItem>
                      <div className="relative h-12">
                        <Lock
                          className={`absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 transition-colors duration-200
                          ${
                            !errors.password && field.value
                              ? "text-foreground"
                              : "text-gray-400"
                          }`}
                        />
                        <FormControl>
                          <Input
                            type={showPassword ? "text" : "password"}
                            {...field}
                            placeholder="Password"
                            className="pl-10 pr-10 h-12 text-[15px] focus:ring-2 focus:ring-gray-300"
                          />
                        </FormControl>

                        <button
                          type="button"
                          onClick={() => setShowPassword(!showPassword)}
                          className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700 transition"
                        >
                          {showPassword ? (
                            <EyeOff className="w-5 h-5" />
                          ) : (
                            <Eye className="w-5 h-5" />
                          )}
                        </button>
                      </div>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                {/* Forgot Password */}
                <div className="flex justify-end">
                  <Link
                    href="#"
                    className="text-sm text-muted-foreground hover:text-foreground"
                  >
                    Forgot password?
                  </Link>
                </div>

                {/* Submit */}
                <Button
                  type="submit"
                  className="w-full bg-foreground text-white hover:bg-gray-800 h-11 text-base shadow-md"
                >
                  Sign In
                </Button>
              </form>
            </Form>
          </CardContent>

          {/* Footer */}
          <CardFooter className="flex flex-col gap-2">
            <Button
              type="button"
              variant="ghost"
              asChild
              className="w-full border-gray-300 text-foreground hover:bg-gray-100"
            >
              <Link href="/register">Sign Up Here</Link>
            </Button>
          </CardFooter>
        </Card>


      </div>
    </main>
  );
}
