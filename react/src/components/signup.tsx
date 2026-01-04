import { Alert, Button, TextField } from "@mui/material";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";

import loadingState from "../store/loading_store";
import userStore from '../store/user_store';
import request_utils from "../utils/request_utils";

import type { SignupForm } from "../types/types";

function Signup() {
  const navigate = useNavigate();
  const { setEmail } = userStore();
  const { setLoading } = loadingState();
  const [pwMatchError, setPwMatchError] = useState<boolean>(false);
  const [signupError, setSignupError] = useState<boolean>(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<SignupForm>();

  const onSubmit = async (data: SignupForm) => {
    setPwMatchError(false);
    setSignupError(false);

    if (data.password != data.password_confirm) {
      setPwMatchError(true);
      throw new Error(`password mismatch`);
    }

    setLoading(true);

    const res_promise = request_utils.requests(
      `${import.meta.env.VITE_API_HOST}/api/signup`,
      "POST",
      {},
      {
        email: data.email,
        password: data.password,
      }
    );
    const res = await res_promise;

    setLoading(false);

    if (res.status != 200) {
      setSignupError(true);
      throw new Error(`signup error`);
    };

    setEmail(data.email);
    navigate("/verify");
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
          sx={{ marginTop: "5%" }}
        >
          Sign Up
        </Button>

        {pwMatchError && (
          <Alert severity="error" sx={{ mt: 2 }}>
            パスワードが一致しません
          </Alert>
        )}
        {signupError && (
          <Alert severity="error" sx={{ mt: 2 }}>
            ユーザ登録に失敗しました
          </Alert>
        )}
      </form>
    </>
  );
};

export default Signup;