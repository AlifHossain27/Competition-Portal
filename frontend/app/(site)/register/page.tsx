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
// import { toast } from "sonner";
import { Mail, Lock, User, IdCard, Eye, EyeOff } from "lucide-react";
import Link from "next/link";

// ⬇️ Import the same reusable Card components
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from "@/components/ui/signInCard";

// ✅ Validation schema
const formSchema = z.object({
  name: z
    .string()
    .min(1, { message: "Name is required." })
    .regex(/^[A-Za-z]+(?:[A-Za-z]*)?$/, {
      message: "Name must not contain digits or spaces.",
    }),
  email: z.string().email({ message: "Please enter a valid email address." }),
  password: z
    .string()
    .min(8, { message: "Password must be at least 8 characters." }),
  universityId: z.string().regex(/^\d{8,}$/, {
    message: "University ID must be at least 8 digits.",
  }),
});

export default function RegisterPage() {
  const router = useRouter();
  const [showPassword, setShowPassword] = useState(false);

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: "",
      email: "",
      password: "",
      universityId: "",
    },
    mode: "onChange",
  });

  const {
    control,
    handleSubmit,
    formState: { errors },
  } = form;

  async function onSubmit(values: z.infer<typeof formSchema>) {
    // Simulated successful registration
    // toast.success("Registration Successful");
    console.log(values);
    router.push("/login");
  }

  return (
    <main className="min-h-screen flex items-center justify-center bg-gradient-to-b from-primary/12 to-background">
      <div className="w-full max-w-md">
        <Card className="border-border bg-card bg-gradient-to-b from-primary/10 to-background shadow-xl">
          {/* Header */}
          <CardHeader>
            <div className="bg-white/60 p-3 rounded-full mb-3 shadow-sm">
              <User className="w-6 h-6 text-gray-700" />
            </div>
            <CardTitle className="text-xl font-semibold text-foreground">
              Create your account
            </CardTitle>
            <CardDescription className="text-center">
              Fill in your details to get started.
            </CardDescription>
          </CardHeader>

          {/* Form Content */}
          <CardContent>
            <Form {...form}>
              <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
                {/* NAME FIELD */}
                <FormField
                  control={control}
                  name="name"
                  render={({ field }) => (
                    <FormItem>
                      <div className="relative h-12">
                        <User
                          className={`absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 transition-colors duration-200
                          ${
                            !errors.name && field.value
                              ? "text-foreground"
                              : "text-gray-400"
                          }`}
                        />
                        <FormControl>
                          <Input
                            type="text"
                            placeholder="Full Name"
                            autoComplete="off"
                            {...field}
                            className="pl-10 pr-3 h-12 text-[15px] focus:ring-2 focus:ring-gray-300"
                          />
                        </FormControl>
                      </div>
                      <FormMessage />
                    </FormItem>
                  )}
                />

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
                            placeholder="Email"
                            autoComplete="off"
                            {...field}
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
                            placeholder="Password"
                            {...field}
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

                {/* UNIVERSITY ID FIELD */}
                <FormField
                  control={control}
                  name="universityId"
                  render={({ field }) => (
                    <FormItem>
                      <div className="relative h-12">
                        <IdCard
                          className={`absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 transition-colors duration-200
                          ${
                            !errors.universityId && field.value
                              ? "text-foreground"
                              : "text-gray-400"
                          }`}
                        />
                        <FormControl>
                          <Input
                            type="text"
                            placeholder="University ID"
                            autoComplete="off"
                            {...field}
                            className="pl-10 pr-3 h-12 text-[15px] focus:ring-2 focus:ring-gray-300"
                          />
                        </FormControl>
                      </div>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                {/* Submit */}
                <Button
                  type="submit"
                  className="w-full bg-foreground text-white hover:bg-gray-800 h-11 text-base shadow-md"
                >
                  Sign Up
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
              <Link href="/login">Back to Login</Link>
            </Button>
          </CardFooter>
        </Card>
      </div>
    </main>
  );
}
