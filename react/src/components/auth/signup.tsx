import { Alert, Button, TextField } from "@mui/material";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";

import type { SignupForm } from "@/src/lib/types";

import RequestHandler from "@/src/lib/request_handler";
import loadingState from "@/src/store/loading_store";
import userStore from '@/src/store/user_store';


function Signup() {
  const { resetUserState } = userStore();
  const { setLoading, resetLoadingState } = loadingState();
  const [signupError, setSignupError] = useState(false);
  const { register, handleSubmit, formState: { errors } } = useForm<SignupForm>();

  useEffect(() => {
    resetUserState();
    resetLoadingState();
  }, []);

  async function onSubmit(data: SignupForm) {
    if (data.password !== data.password_confirm) {
      setSignupError(true);
      throw new Error("signup error");
    };

    setLoading(true);
    setSignupError(false);

    const requests = new RequestHandler();
    const signup_res = await requests.post(
      `/api/signup`,
      { email: data.email, password: data.password }
    );

    if (signup_res.status != 200) {
      setSignupError(true);
      setLoading(false);
      throw new Error("signup error");
    };

    setLoading(false);
  };

  return (
    <>
      <form onSubmit={handleSubmit(onSubmit)}>
        <TextField
          label="メールアドレス"
          fullWidth
          margin="normal"
          {...register("email", {
            required: "メールアドレスは必須です",
          })}
          error={!!errors.email}
          helperText={errors.email?.message}
        />

        <TextField
          label="パスワード"
          type="password"
          fullWidth
          margin="normal"
          {...register("password", {
            required: "パスワードは必須です",
          })}
          error={!!errors.password}
          helperText={errors.password?.message}
        />

        <TextField
          label="パスワード(確認用)"
          type="password"
          fullWidth
          margin="normal"
          {...register("password_confirm", {
            required: "パスワード(確認用)は必須です",
          })}
          error={!!errors.password_confirm}
          helperText={errors.password_confirm?.message}
        />

        <Button
          type="submit"
          fullWidth
          variant="contained"
          sx={{ mt: 3 }}
        >
          サインアップ
        </Button>

        {signupError && (
          <Alert severity="error" sx={{ mt: 2 }}>
            サインアップに失敗しました
          </Alert>
        )}
      </form>
    </>
  );
};

export default Signup;
