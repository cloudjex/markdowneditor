import { Breadcrumbs, Link } from '@mui/material';
import { useLocation } from 'react-router-dom';

import userStore from '../store/user_store';
import tree_utils from '../utils/tree_utils';

import type { Tree } from "../types/types";

function Breadcrumb() {
  const { tree } = userStore();
  const location = useLocation();

  const searchParams = new URLSearchParams(location.search);
  const url_node_id = searchParams.get('node_id');

  let parentNodes: Tree[] = [];
  if (url_node_id && tree) {
    const parents = tree_utils.get_parent_node_ids(url_node_id);
    const this_node = tree_utils.get_node(tree, url_node_id);

    const filter_targets = parents.map((id) => tree_utils.get_node(tree, id));
    parentNodes = filter_targets.filter((node) => node !== null);
    if (this_node) {
      parentNodes.push(this_node);
    };
  };

  if (parentNodes) {
    return (
      <Breadcrumbs separator="›" aria-label="breadcrumb" sx={{ mt: 1 }}>
        {parentNodes.map((node, index) => (
          <Link
            key={node.id}
            underline="none"
            color={index === parentNodes.length - 1 ? "textDisabled" : "textSecondary"}
            href={index === parentNodes.length - 1 ? undefined : `/main?node_id=${node.id}`}
            aria-current={index === parentNodes.length - 1 ? "page" : undefined}
          >
            {node.label}
          </Link>
        ))}
      </Breadcrumbs>
    );
  };
}

export default Breadcrumb;
