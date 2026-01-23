import { Alert, Button, TextField } from "@mui/material";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";

import RequestHandler from "../../lib/request_handler";
import loadingState from "../../store/loading_store";
import userStore from '../../store/user_store';

import type { SigninForm, SigninResponse, TreeResponse } from "../../lib/types";

function Signin() {
  const navigate = useNavigate();
  const { setEmail, setIdToken, resetUserState, setNodeTree } = userStore();
  const { setLoading, resetLoadingState } = loadingState();
  const [signinError, setSigninError] = useState(false);

  const requests = new RequestHandler();

  useEffect(() => {
    resetUserState();
    resetLoadingState();
  }, []);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<SigninForm>();

  async function onSubmit(data: SigninForm) {
    setLoading(true);
    setSigninError(false);

    const signin_res_promise = requests.post<SigninResponse>(
      `${import.meta.env.VITE_API_HOST}/api/signin`,
      { email: data.email, password: data.password }
    );
    const signin_res = await signin_res_promise;

    if (signin_res.status != 200) {
      setSigninError(true);
      setLoading(false);
      throw new Error("signin error");
    };

    requests.id_token = signin_res.body.id_token;
    const tree_res_promise = requests.get<TreeResponse>(
      `${import.meta.env.VITE_API_HOST}/api/trees`,
    );
    const tree_res = await tree_res_promise;

    setLoading(false);
    setIdToken(signin_res.body.id_token);
    setEmail(signin_res.body.email);
    setNodeTree(tree_res.body.node_tree);
    navigate(`/main?id=${tree_res.body.node_tree.id}`);
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