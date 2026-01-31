import { Alert, Button, TextField } from "@mui/material";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";

import type { SigninForm, SigninResponse, Tree } from "@/src/lib/types";

import RequestHandler from "@/src/lib/request_handler";
import loadingState from "@/src/store/loading_store";
import userStore from '@/src/store/user_store';


function Signin() {
  const navigate = useNavigate();
  const { setEmail, setIdToken, resetUserState, setTree } = userStore();
  const { setLoading, resetLoadingState } = loadingState();
  const [signinError, setSigninError] = useState(false);
  const { register, handleSubmit, formState: { errors } } = useForm<SigninForm>();

  const requests = new RequestHandler();

  useEffect(() => {
    resetUserState();
    resetLoadingState();
  }, []);

  async function onSubmit(data: SigninForm) {
    setLoading(true);
    setSigninError(false);

    const signin_res = await requests.post<SigninResponse>(
      `${import.meta.env.VITE_API_HOST}/api/signin`,
      { email: data.email, password: data.password }
    );

    if (signin_res.status != 200) {
      setSigninError(true);
      setLoading(false);
      throw new Error("signin error");
    };

    requests.id_token = signin_res.body.id_token;
    const tree_res = await requests.get<Tree>(
      `${import.meta.env.VITE_API_HOST}/api/tree`,
    );

    setLoading(false);
    setIdToken(signin_res.body.id_token);
    setEmail(data.email);
    setTree(tree_res.body);
    navigate(`/main/${tree_res.body.node_id}`);
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
          sx={{ mt: 3 }}
        >
          サインイン
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