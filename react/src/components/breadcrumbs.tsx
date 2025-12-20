import Breadcrumbs from '@mui/material/Breadcrumbs';
import Link from '@mui/material/Link';
import { useLocation } from 'react-router-dom';

import userStore from '../store/user_store';
import utils from '../utils/utils';

import type { TreeNode } from "../types/tree";

function Breadcrumb() {
  const { tree } = userStore();
  const location = useLocation();

  const searchParams = new URLSearchParams(location.search);
  const url_node_id = searchParams.get('node_id');

  let parentNodes: TreeNode[] = [];
  if (url_node_id && tree) {
    const parents = utils.get_parent_node_ids(url_node_id);
    const this_node = utils.get_node(tree, url_node_id);

    const filter_targets = parents.map((id) => utils.get_node(tree, id));
    parentNodes = filter_targets.filter((node) => node !== null);
    if (this_node) {
      parentNodes.push(this_node);
    };
  };

  if (parentNodes) {
    return (
      <Breadcrumbs aria-label="breadcrumb" sx={{ mb: 2 }}>
        {parentNodes.map((node, index) => (
          <Link
            key={node.id}
            underline="hover"
            color={index === parentNodes.length - 1 ? "text.primary" : "inherit"}
            href={`/main?node_id=${node.id}`}
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
