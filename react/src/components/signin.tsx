import { Alert, Button, TextField } from "@mui/material";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";

import loadingState from "../store/loading_store";
import userStore from '../store/user_store';
import utils from "../utils/utils";

import type { SigninForm } from "../types/types";

function Signin() {
  const navigate = useNavigate();
  const { setEmail, setIdToken, resetUserState } = userStore();
  const { setLoading, resetLoadingState } = loadingState();

  const [signinError, setSigninError] = useState(false);

  useEffect(() => {
    resetUserState();
    resetLoadingState();
  }, []);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<SigninForm>();

  const onSubmit = async (data: SigninForm) => {
    setLoading(true);
    setSigninError(false);

    const res_promise = utils.requests(
      `${import.meta.env.VITE_API_HOST}/api/signin`,
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
      setSigninError(true);
      throw new Error(`signin error`);
    };

    const body = res.body as { email: string, id_token: string };
    setEmail(body.email);
    setIdToken(body.id_token);
    navigate("/main?node_id=/Nodes");
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

        <Button
          type="submit"
          fullWidth
          variant="contained"
          sx={{ marginTop: "5%" }}
        >
          Sign In
        </Button>

        {signinError && (
          <Alert severity="error" sx={{ mt: 2 }}>
            メールアドレスまたはパスワードが正しくありません
          </Alert>
        )}
      </form>
    </>
  );
};

export default Signin;